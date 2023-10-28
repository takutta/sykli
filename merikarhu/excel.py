import pandas as pd
import numpy as np
import os
import json
from loggaus import log, exception


@exception("")
def lataa_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Virhe ladattaessa tiedostoa {filename}: {e}")
            return None
    else:
        print(f"Tiedostoa {filename} ei ole olemassa.")
        return None

    # @exception("")
    # def excel_import(tiedosto):
    #     pd.set_option("display.max_columns", None)
    #     data = pd.read_csv(
    #         tiedosto, sep=",", encoding="latin1"
    #     )  # Olettaen, että data on CSV-tiedostossa

    #     # print(data)
    #     excel_pvm = data.iloc[0, 2]
    #     paivat = int(data.iloc[0, 1])
    #     paivystys = True if (data.iloc[0, 2]) == "Kyllä" else False

    #     excel_asetukset = {"pvm": excel_pvm, "paivat": paivat, "paivystys": paivystys}

    #     @exception("")
    #     def poista_tyhjat(df):
    #         return df.dropna(how="all", inplace=True)

    #     @exception("")
    #     def ryhmat_listaksi(df):
    #         df["ryhmat"] = df["ryhmat"].apply(
    #             lambda x: [i.strip() for i in str(x).split(",")]
    #         )
    #         return df

    @exception("")
    def muokkaa_dictit(lista):
        uusi_lista = []
        for dicti in lista:
            uusi_dict = {}
            uusi_dict.update(dicti)
            uusi_dict["ajat"] = {k: v for k, v in uusi_dict.items() if k.isdigit()}
            for k in uusi_dict["ajat"]:
                uusi_dict.pop(k, None)
            uusi_lista.append(uusi_dict)
        return uusi_lista

    # def muokkaa_lasten_dict(lista):
    #     uusi_lista = []
    #     for dicti in lista:
    #         uusi_dict = {}
    #         uusi_dict.update(dicti)
    #         uusi_dict["ajat"] = {
    #             int(k): [
    #                 "{}-{}".format(tulo, lahto)
    #                 for tulo, lahto in zip(
    #                     v.split("-")[0].split(","), v.split("-")[1].split(",")
    #                 )
    #             ]
    #             for k, v in uusi_dict.items()
    #             if k.isdigit() and "-" in v
    #         }
    #         for k in list(
    #             uusi_dict.keys()
    #         ):  # List conversion necessary to prevent dictionary size change during iteration error.
    #             if k.isdigit():
    #                 uusi_dict.pop(k)
    #         uusi_lista.append(uusi_dict)
    #     return uusi_lista

    # ryhmat_omat = data.iloc[:, 5:7]
    # poista_tyhjat(ryhmat_omat)
    # ryhmat_omat = ryhmat_listaksi(ryhmat_omat)
    # ryhmat_omat_dict = ryhmat_omat.to_dict("records")

    # def yhdista_ajat(df, tulo, lahto):
    #     df[tulo[0]] = df[tulo].astype(str) + "-" + df[lahto].astype(str)
    #     df = df.drop(tulo, axis=1)
    #     df = df.drop(lahto, axis=1)
    #     df.replace("-", "", inplace=True)
    #     return df

    # lapset = data.iloc[:, 9:28]
    # lapset.fillna("", inplace=True)
    # lapset.replace("P", "", inplace=True)
    # lapset.replace("", np.nan, inplace=True)
    # poista_tyhjat(lapset)
    # lapset.replace(np.nan, "", inplace=True)

    # for i in range(7):
    #     lapset = yhdista_ajat(lapset, f"{i}_tulo", f"{i}_lahto")
    # lapset_dict = lapset.to_dict("records")
    # lapset_dict = muokkaa_lasten_dict(lapset_dict)

    # ryhmat_kaikki = list(set(lapset["ryhma"].str.capitalize()))

    # tyontekijat = data.iloc[:, 32:37]
    # tyontekijat.rename(columns={"kutsumanimi.1": "kutsumanimi"}, inplace=True)
    # tyontekijat.rename(columns={"kokonimi.1": "kokonimi"}, inplace=True)
    # tyontekijat.rename(columns={"ryhma.1": "ryhma"}, inplace=True)
    # poista_tyhjat(tyontekijat)
    # tyontekijat.fillna("", inplace=True)
    # tyontekijat["vastuullinen"] = np.where(
    #     tyontekijat["vastuullinen"] == "Kyllä", True, ""
    # )

    # tyontekijat_dict = tyontekijat.to_dict("records")

    # return (
    #     ryhmat_omat_dict,
    #     ryhmat_kaikki,
    #     lapset_dict,
    #     tyontekijat_dict,
    #     excel_asetukset,
    # )


@exception("")
def tt_asetukset_synkka(titania_tt: list, excel_data: dict, pk_nimi: str):
    if len(excel_data["tyontekijat"]) != 0:
        for ex_tt in excel_data["tyontekijat"]:
            for ti_tt in titania_tt:
                if "nimi" in ex_tt and ex_tt["nimi"] == ti_tt["kokonimi"]:
                    if "kutsumanimi" in ex_tt:
                        ti_tt["kutsumanimi"] = ex_tt["kutsumanimi"]
                    if "ryhma" in ex_tt:
                        ti_tt["ryhma"] = ex_tt["ryhma"]
                    if "vastuullinen" in ex_tt:
                        ti_tt["vastuullinen"] = ex_tt["vastuullinen"]
                    if "nimike" in ex_tt:
                        ti_tt["nimike"] = ex_tt["nimike"]
                    if "kiertopohja" in ex_tt:
                        ti_tt["kiertopohja"] = ex_tt["kiertopohja"]
                    if "prosentti" in ex_tt:
                        ti_tt["prosentti"] = ex_tt["prosentti"]
                    if "aktiivinen" in ex_tt:
                        ti_tt["aktiivinen"] = ex_tt["aktiivinen"]

    excel_data["tyontekijat"] = titania_tt
    excel_data["pk_nimi"] = pk_nimi

    for lapsi in excel_data["lapset"]:
        if "ajat" in lapsi:
            # Muuta ajat-sanakirjan avaimet kokonaisluvuiksi
            lapsi["ajat"] = {int(k): v for k, v in lapsi["ajat"].items()}
            # Muuta kaikki hoitoajat kaksoispisteet pisteiksi

        for paiva, hoitoajat in lapsi["ajat"].items():
            if hoitoajat != "P":
                lapsi["ajat"][paiva] = [
                    [aika.replace(":", ".") for aika in aikavali]
                    for aikavali in hoitoajat
                ]
            else:
                lapsi["ajat"][paiva] = hoitoajat
    return excel_data


@exception("")
def excel_export(data: dict, osoite: str) -> None:
    with open(osoite, "w") as tiedosto:
        json.dump(data, tiedosto)
