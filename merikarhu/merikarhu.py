from tkinter import *
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os, sys, time
import titania as ti
import excel as ex
from tarvetaulukko import luo_tarvetaulukko
from loggaus import log, exception


class GUI(Tk):
    def __init__(self):
        super().__init__()

        # data
        self.titaniat = []
        self.txt_loytyi = 0
        self.txt_maara = int(sys.argv[1]) if len(sys.argv) > 1 else 2
        self.data = None

        self.pvm_titania = ""
        self.pk_nimi = ""

        self.excel_loytyi = False
        self.excel_data = ""

        # vanha
        self.titania_vanha = BooleanVar()
        self.excel_vanha = BooleanVar()
        self.vanha_loytyi = True

        # muut
        self.peukku_id = None

        # watchdog
        self.watchdog = None
        self.watch_paths = [
            os.path.join(os.path.expanduser("~"), "merikarhu", "input"),
            r"c:\tyko2000\work",
        ]
        self.update_watch_paths()
        self.start_watchdog()

        # gui
        self.title("Merikarhu")
        self.resizable(False, False)
        self.iconbitmap("merikarhu.ico")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = 0
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_widgets()
        if self.vanha_loytyi:
            self.vanha_ikkuna()

        self.poista_txt()

    @exception("")
    def create_widgets(self):
        log("debug", "Luodaan widgetit")
        self.canvas = Canvas(self, width=800, height=600, bg="SystemButtonFace")
        self.canvas.pack(fill=BOTH, expand=True)

        self.background_image = PhotoImage(file="hylje.png")
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

        self.log_text = ""
        self.log_text_id = self.canvas.create_text(
            5,
            0,
            text=self.log_text,
            font=("Segoe UI", 14),
            fill="black",
            anchor="nw",
            width=780,
        )
        self.log("Hei! Olen Merikarhu!")
        self.log("Hakisitko minulle Titania-listat sekä tiedot Hoitoajat Excelistä?")

        button_frame = Frame(self.canvas)
        self.button = Button(
            button_frame,
            text="Klikkaa, kun tiedostot ovat löytyneet",
            font=("Segoe UI", 16),
            command=self.button_clicked,
        )
        self.button.pack(pady=0)
        self.canvas.create_window(400, 580, anchor=SE, window=button_frame)
        self.button.config(state=DISABLED)

    @exception("")
    def vanha_ikkuna(self):
        checkbox_frame = Frame(self.canvas)
        self.canvas.create_window(520, 580, anchor=SW, window=checkbox_frame)

        checkbox = Checkbutton(
            checkbox_frame,
            variable=self.titania_vanha,
            text="Käytä vanhaa Titaniaa",
            font=("Segoe UI", 16),
            command=self.titania_vanha_clicked,
        )
        checkbox.pack(side=BOTTOM, anchor=SW)

        checkbox = Checkbutton(
            checkbox_frame,
            variable=self.excel_vanha,
            text="Käytä vanhaa Exceliä",
            font=("Segoe UI", 16),
            command=self.excel_vanha_clicked,
        )
        checkbox.pack(side=BOTTOM, anchor=SW)

    @exception("")
    def titania_vanha_clicked(self):
        if self.titania_vanha.get():
            excel_path = os.path.join(
                os.path.expanduser("~"), "merikarhu", "output", "merikarhu_output.json"
            )
            excel_data = ex.lataa_json(excel_path)
            log("debug", f"Ladataan työvuorotiedot Excelistä: {excel_path}")

            self.titaniat = [excel_data["tyontekijat"]]
            for tt in self.titaniat[0]:
                tt["ajat"] = {int(paiva): arvo for paiva, arvo in tt["ajat"].items()}
            self.pvm_titania = excel_data["pvm_titania"]
            self.pk_nimi = excel_data["pk_nimi"]
            self.txt_loytyi = self.txt_maara
            self.check_files_and_show_button()

        else:
            self.pvm_titania = ""
            self.titaniat = []
            self.txt_loytyi = 0
            self.check_files_and_show_button()

    @exception("")
    def excel_vanha_clicked(self):
        if self.excel_vanha.get():
            self.excel_loytyi = True
            excel_path = os.path.join(
                os.path.expanduser("~"), "merikarhu", "output", "merikarhu_output.json"
            )
            log("debug", f"Ladataan hoitoaikatiedot Excelistä: {excel_path}")
            self.excel_data = ex.lataa_json(excel_path)
            for tt in self.excel_data["tyontekijat"]:  # nimien keyt titania-sopivaksi
                tt["nimi"] = tt.pop("kokonimi", "default")
            self.check_files_and_show_button()
        else:
            self.excel_loytyi = False
            self.excel_data = ""
            self.check_files_and_show_button()

    @exception("")
    def log(self, message):
        self.log_text += f"\n{message}"
        self.canvas.itemconfig(self.log_text_id, text=self.log_text)

    @exception("")
    def lisaa_peukku(self):
        img = PhotoImage(file="peukku.png")
        self.peukku_id = self.canvas.create_image(540, 190, anchor="nw", image=img)
        self.peukku = img

    @exception("")
    def poista_peukku(self):
        if self.peukku_id is not None:
            self.canvas.delete(self.peukku_id)
            self.peukku_id = None

    @exception("")
    def update_watch_paths(self):
        """Poista polut, jotka eivät ole olemassa"""
        self.watch_paths = [path for path in self.watch_paths if os.path.exists(path)]

    @exception("")
    def start_watchdog(self):
        if self.watchdog is None:
            log("debug", "Käynnistetään Watchdog")
            self.watchdog = Watchdog(paths=self.watch_paths, logfunc=self.log, gui=self)
            self.watchdog.start()

    @exception("")
    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log("Watchdog pysäytetty")
        else:
            self.log("Watchdog ei ole käynnissä")

    @exception("")
    def poista_txt(self):
        log("debug", r"Poistetaan titaniat c:\tyko2000\work")
        [
            os.remove(os.path.join(r"c:\tyko2000\work", tiedostonimi))
            for tiedostonimi in os.listdir(r"c:\tyko2000\work")
            if os.path.isfile(os.path.join(r"c:\tyko2000\work", tiedostonimi))
            and tiedostonimi.endswith(".txt")
        ]

    @exception("")
    def process_data(self):
        log("debug", "Prosessoidaan tiedostot")
        if len(self.titaniat) == 1 or self.titania_vanha.get():
            titania_tt = self.titaniat[0]
        else:
            # titanioiden yhdistäminen
            titania_tt = ti.yhdista_tyontekijat(self.titaniat)
        log("debug", "Synkataan työntekijä-tiedot Exceliltä tulevan jsonin kanssa")
        self.data = ex.tt_asetukset_synkka(titania_tt, self.excel_data, self.pk_nimi)
        self.data["pvm_titania"] = self.pvm_titania

    @exception("")
    def show_button(self):
        self.button.config(text="Aloita listojen luonti", state=NORMAL)

    @exception("")
    def button_clicked(self):
        log("debug", "Luodaan tarvetaulukko")
        luo_tarvetaulukko(self.data)

    def create_output_file(self):
        output_filepath = os.path.join(
            os.path.expanduser("~"), "merikarhu", "output", "merikarhu_output.json"
        )
        log("debug", f"Exportataan json Exceliä varten: {output_filepath}")

        ex.excel_export(self.data, output_filepath)

    @exception("")
    def check_files_and_show_button(self):
        if self.txt_loytyi == self.txt_maara and self.excel_loytyi:
            self.process_data()
            self.create_output_file()
            self.show_button()
            self.lisaa_peukku()

        else:
            self.button.config(state=DISABLED)
            self.button.config(text="Klikkaa, kun tiedostot ovat löytyneet")
            self.poista_peukku()

    @exception("")
    def process_titania_file(self, file_path):
        if self.txt_loytyi < self.txt_maara:
            self.txt_loytyi += 1
            self.log(
                f"Titania {self.txt_loytyi}/{self.txt_maara} löytyi: {os.path.splitext(os.path.basename(file_path))[0]}"
            )

            self.get_titania_data(file_path)

        elif self.txt_loytyi == self.txt_maara:
            self.log(
                f"Titania {self.txt_loytyi}/{self.txt_maara} korvattu: {os.path.splitext(os.path.basename(file_path))[0]}"
            )
            self.get_titania_data(file_path)

    @exception("")
    def get_titania_data(self, file_path):
        """kerätään titania data ja poistetaan tiedosto"""
        time.sleep(1)
        df, pvm_titania, pk_nimi = ti.titania_import(file_path)
        self.pvm_titania = pvm_titania
        self.pk_nimi = pk_nimi
        tt = ti.df_to_json(df)
        self.titaniat.append(tt)
        self.check_files_and_show_button()
        time.sleep(1)
        os.remove(file_path)

    @exception("")
    def process_excel_file(self, file_path):
        # Tiedostotyypin mukainen käsittely
        if self.excel_loytyi:
            self.log(f"Vanhat Excel-tiedot korvattu uusilla.")
        else:
            self.excel_loytyi = True
            self.log(f"Excel löytyi.")
        log("debug", f"Ladataan tiedot Excel jsonista: {file_path}")
        self.excel_data = ex.lataa_json(file_path)
        self.check_files_and_show_button()


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, paths=None, patterns="*", logfunc=print, gui=None):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.paths = paths or []
        self.setup_watchers()
        self.log = logfunc
        self.gui = gui

    @exception("")
    def setup_watchers(self):
        # Poista polut, jotka eivät ole olemassa
        self.paths = [path for path in self.paths if os.path.exists(path)]
        for path in self.paths:
            self.schedule(self, path=path, recursive=False)

    @exception("")
    def on_created(self, event):
        # Tiedoston luomistapahtuma
        self.process_file(event.src_path)

    @exception("")
    def process_file(self, file_path):
        if file_path.endswith(".txt"):  # titania
            self.gui.process_titania_file(file_path)
        elif file_path.endswith(".json"):  # excel
            self.gui.process_excel_file(file_path)


if __name__ == "__main__":
    log("debug", "Merikarhu käynnistyy")
    GUI().mainloop()
