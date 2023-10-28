import webbrowser, os, re, shutil
from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import plot
from datetime import datetime, timedelta
from loggaus import log, exception


@exception("")
def plotly_esityo(rivit):
    klo = []
    kerroin = []
    vastuulliset = []
    muutKerroin = []

    for sarake in rivit[1:]:
        klo.append(sarake[0])
        kerroin.append(sarake[3])

        numerot = re.findall(r"[0-9]+", sarake[4])
        vastuulliset_num, muut_num, tarve_num = [int(numero) for numero in numerot]
        vastuulliset.append(vastuulliset_num)
        muutKerroin.append(vastuulliset_num + muut_num * 0.5)

    return klo, kerroin, vastuulliset, muutKerroin


@exception("")
def viivat(klo, kerroin, tyontekijat, muutKerroin, ryhma_nimi):
    pio.templates.default = "seaborn"

    kellonajat = [datetime.strptime(aika, "%H:%M") for aika in klo]

    # Määritä x-akselin merkinnät puolen tunnin välein
    x_tickvals = []
    x_ticktext = []

    if len(kellonajat) != 0:
        current_time = kellonajat[0]
    else:
        return False

    # Etsi lähin tasa- tai puolituntinen alku- ja loppuaika
    if current_time.minute >= 30:
        current_time = current_time.replace(minute=30, second=0)
    else:
        current_time = current_time.replace(minute=0, second=0)

    # Alusta x-akselin merkinnät
    while current_time <= kellonajat[-1]:
        x_tickvals.append(current_time)
        x_ticktext.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=muutKerroin,
            name="Kerroin + ½ muut",
            marker=dict(color="gray"),
            line=dict(color="gray", shape="hv", dash="dot"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=tyontekijat,
            name="Vastuulliset",
            marker=dict(color="green"),
            line=dict(color="green", shape="hv"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=kerroin,
            name="Kerroin",
            marker=dict(color="black"),
            line=dict(color="black", shape="hv"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        )
    )

    fig.update_layout(
        yaxis=dict(dtick=1),  # Vain kokonaislukujen kohdalla
        xaxis=dict(
            tickmode="array", tickvals=x_tickvals, ticktext=x_ticktext, tickangle=45
        ),
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.16,
                showarrow=False,
                text=ryhma_nimi,
                font=dict(size=24, color="black"),
            )
        ],
        hovermode="x unified",
        legend=dict(traceorder="reversed"),
    )
    return plot(fig, output_type="div", include_plotlyjs=False)


@exception("")
def format_date(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


@exception("")
def html_luonti(template_nimi, html_nimi, data, asetukset):
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_date"] = format_date
    template = env.get_template(template_nimi)

    # for k, v in asetukset.items():
    #     print("key:", k, "value:", v)

    html = template.render(data=data, asetukset=asetukset)
    file_name = os.path.join("build", html_nimi)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)
    return file_name


@exception("")
def html_avaus(nimi):
    filepath = "file://" + os.path.abspath(nimi)
    webbrowser.open_new_tab(filepath)


@exception("")
def arkistointi(asetukset):
    # lopeta, jos arkistointi ei päällä
    if not asetukset["arkistointi"]["arkistointi"]:
        return

    tiimi = (
        str(asetukset["arkistointi"]["tiimin_nimi"])
        .encode("iso-8859-1")
        .decode("unicode_escape")
    )

    pvm = asetukset["viikon_paivat"][0]
    vuosi, viikko, pv = pvm.isocalendar()
    user_folder = os.path.expanduser("~")

    destination_path = os.path.join(
        user_folder, "Jyväskylän kaupunki", f"{tiimi} - Tiedostot"
    )
    # Jos kansio löytyy
    if os.path.isdir(destination_path):
        destination_path = os.path.join(
            destination_path, "General", "Sykli", str(vuosi)
        )
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        source = os.path.join(os.path.expanduser("~"), "merikarhu", "build")
        shutil.copytree(source, destination_path, dirs_exist_ok=True)
    else:
        log(
            "warning",
            f"Arkistointi on päällä, mutta synkattavaa kansiota ei löytynyt: {destination_path}",
        )


@exception("")
def siirra_kansiot(lista_kansioista, kohde):
    for kansio in lista_kansioista:
        shutil.copytree(
            kansio, os.path.join(kohde, os.path.basename(kansio)), dirs_exist_ok=True
        )


@exception("")
def build_reset():
    shutil.rmtree("./build")
    os.makedirs("./build")


if __name__ == "__main__":
    # asetukset = {"viikon_paivat": [datetime.now()],
    #              "ero": 0, "pk_nimi":"Tapiolan päiväkoti",
    #              'arkistointi': {"arkistointi":True,
    #                              "tiimin_nimi":"Kukkumäen ja Kypärämäen päiväkodit",
    #                              "kansio":"Sykli"}}
    # arkistointi(asetukset)

    # kohde = "./build/Aputiedostot/vk_" + asetukset["viikon_paivat"][0].strftime("%V")
    kohde = "./build/Aputiedostot/vk_34"
    siirra_kansiot(["./other/css", "./other/js"], kohde)
