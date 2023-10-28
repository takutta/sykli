import pandas as pd
import numpy as np
from re import match, sub
from loggaus import log, exception


@exception("")
def titania_import(tiedoston_nimi):
    pd.set_option("display.max_columns", 7)
    pd.set_option("display.max_rows", 70)
    pd.set_option("display.width", None)
    pd.set_option("display.unicode.ambiguous_as_wide", True)

    koko_tiedosto = pd.read_csv(
        tiedoston_nimi, sep="\t", encoding="latin1", header=None, on_bad_lines="skip"
    )
    pvm = str(koko_tiedosto.copy().iloc[2, 9]).strip()[:8]
    pk_nimi = sub(r"\d+", "", koko_tiedosto.copy().iloc[1, 2]).strip()

    df_csv = pd.read_csv(
        tiedoston_nimi, sep="\t", encoding="latin1", header=None, skiprows=5
    )
    df = df_csv.copy()

    def remove_extra_spaces(cell):
        if pd.notnull(cell) and isinstance(cell, str):
            stripped_cell = cell.strip()
            if stripped_cell:
                return " ".join(stripped_cell.split())
            else:
                return np.nan
        else:
            return cell

    def add_nan(cell):
        if isinstance(cell, str):
            stripped_cell = cell.strip()
            if not stripped_cell:
                return np.nan
        return cell

    def remove_dots(cell):
        if isinstance(cell, str):
            return cell.replace(
                ".", ""
            ).strip()  # Poista pisteet solun alusta ja lopusta
        else:
            return cell

    df = df.applymap(remove_extra_spaces)
    df = df.replace("#", "", regex=True)
    df.drop(df.columns[-2:], axis=1, inplace=True)

    df = df.applymap(remove_dots)

    df.dropna(axis=1, how="all", inplace=True)
    df.dropna(axis=0, how="all", inplace=True)
    # replace empty strings with np.nan

    df.reset_index(drop=True, inplace=True)

    df.iloc[:, 0].fillna(method="ffill", inplace=True)
    df = df.fillna("")

    # Täytä ensimmäisen sarakkeen puuttuvat arvot edellisellä voimassaolevalla arvolla
    return df, pvm, pk_nimi


@exception("")
def hae_kutsumanimi(nimi):
    sanat = nimi.split()
    if len(sanat) == 1:
        return sanat[0]
    toinen = sanat[1]
    ensimmainen = sanat[0]
    kutsumanimi = toinen + " " + ensimmainen
    return kutsumanimi


@exception("")
def siisti_rivit(rivit):
    return [
        rivi.replace("\\", "S")
        for rivi in rivit
        # ei poistetakaan käyttäjiä joilla ei ole hoitoaikoja
        # if match(r"^[^0-9:]*;+ *$", rivi) is None and rivi != ""
    ]


@exception("")
def luo_tyontekija(csv):
    tyontekija = {
        "kokonimi": csv[0],
        "kutsumanimi": hae_kutsumanimi(csv[0]),
        "ajat": luo_ajat(csv[1:]),
    }

    return tyontekija


@exception("")
def luo_ajat(ajat):
    result = {}
    for i, aika in enumerate(ajat):
        stripped_aika = aika.strip()
        if stripped_aika not in ["V", "T", ".", ""]:
            if stripped_aika.startswith(("K ", "S ")) or ":" in stripped_aika:
                if ":" in stripped_aika:
                    result[i] = [stripped_aika.replace(":", ".")]
                else:
                    result[i] = [stripped_aika.replace(" :", " ").replace(":", ".")]
            else:
                result[i] = [stripped_aika[2:]]
    final = {}
    for k, v in result.items():
        final[k] = [[], []]
        for aikavali in v:
            prefix = ""  # Aloitetaan ilman etuliitettä
            if aikavali.startswith(("K ", "S ")):
                prefix = aikavali[0:2]  # Tallennetaan etuliite, jos se on olemassa
                aikavali = aikavali[2:]  # Poistetaan etuliite itse aikavälistä
            if "-" in aikavali:
                osat = aikavali.split("-")
                final[k][0].append(
                    prefix + osat[0].strip().replace(":", ".")
                )  # Lisää tulo ensimmäiseen listaan etuliitteellä
                if len(osat) > 1:
                    final[k][1].append(
                        prefix + osat[1].strip().replace(":", ".")
                    )  # Lisää lähtö toiseen listaan etuliitteellä
    return final


@exception("")
def lisaa_ajat(tyontekija, csv):
    uudet_ajat = luo_ajat(csv[1:])
    for i, uusi_aika in uudet_ajat.items():
        if i not in tyontekija["ajat"]:
            tyontekija["ajat"][i] = [[], []]
        for j in range(2):  # 0 for arrival times, 1 for departure times
            for aika in uusi_aika[j]:
                if aika not in tyontekija["ajat"][i][j]:
                    tyontekija["ajat"][i][j].append(aika)
    return tyontekija


@exception("")
def df_to_json(df):
    df = df.applymap(str)
    rivit = df.values.tolist()
    rivit = [";".join(rivi) for rivi in rivit]  # Muunna rivit merkkijonoiksi
    siistityt_rivit = rivit
    siistityt_rivit = siisti_rivit(rivit)
    tyontekijat = []
    for rivi in siistityt_rivit:
        csv = rivi.split(";")
        nimi = csv[0]
        if nimi == "nimi":
            continue
        tyontekija = next(
            (
                tyontekija
                for tyontekija in tyontekijat
                if tyontekija["kokonimi"] == nimi
            ),
            None,
        )
        if tyontekija is None:
            tyontekija = luo_tyontekija(csv)
            tyontekijat.append(tyontekija)
        else:
            tyontekija = lisaa_ajat(tyontekija, csv)
    return tyontekijat


@exception("")
def yhdista_tyontekijat(listat):
    data_dict = {}
    for yksi_lista in listat:
        for item in yksi_lista:
            if item["kokonimi"] not in data_dict:
                data_dict[item["kokonimi"]] = item
            else:
                data_dict[item["kokonimi"]]["ajat"].update(item["ajat"])

    return list(data_dict.values())


@exception("")
def tt_asetukset_synkka(tyontekijat, asetukset):
    tt_lista = []
    for tyontekija in tyontekijat:
        for asetus in asetukset:
            if tyontekija["kokonimi"] == asetus["kokonimi"]:
                tyontekija["kutsumanimi"] = asetus["kutsumanimi"]
                tyontekija["vastuullinen"] = asetus["vastuullinen"]
                tyontekija["ryhma"] = asetus["ryhma"]
                tt_lista.append(tyontekija)
                break
    return tyontekijat


if __name__ == "__main__":
    df1, pvm, pk_nimi = titania_import(r"./Hoitoajat/TAP01133.txt")
    # print(pvm)
    # print(pk_nimi)
    # print(df1)
    tt1 = df_to_json(df1)
    for key in tt1:
        print(key["kokonimi"])
    # print(tt1)
