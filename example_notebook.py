import marimo

__generated_with = "0.1.76"
app = marimo.App()


@app.cell
def __():
    import marimo as mo

    mo.md("""# Beispiel-Notebook mit Marimo
    Dieses interaktive Skript baut eine HTTP-Verbindung auf und analysiert die Antwort, die aus JSON-Daten besteht.""")
    return mo,


@app.cell
def __(mo):
    mo.accordion({"Mehr Informationen zu diesem Notebook": ("...")})
    return


@app.cell
def __(mo):
    import requests
    data = requests.get('https://ipinfo.io')
    mo.md(f"""Status Code: {data.status_code}, Antwort des Servers:

        {data.text}""")
    return data, requests


@app.cell
def __(data, mo):
    json_data = data.json()
    loc = json_data['loc']
    ip = json_data['ip']
    city = json_data['city']
    mo.md(f"""Hole die JSON-Daten aus dem Request und extrahiere nur die Location-Daten:

        {ip} kommt aus {city} ({loc.split(",")})""")
    return city, ip, json_data, loc


@app.cell
def __(mo):
    zoomfaktor = mo.ui.slider(7, 17, value=8, label=f"Zoomfaktor: ")
    return zoomfaktor,


@app.cell
def __(zoomfaktor):
    zoomfaktor
    return


@app.cell
def __(zoomfaktor):
    import math

    # Source: https://stackoverflow.com/a/28530369/18073555

    def deg2num(lat_deg, lon_deg, zoom):
        """Calculate tile numbers for OpenStreetMap images from given geo coordinates."""
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def get_osm_image(coordinates):
        coordinates = [float(x) for x in coordinates]
        x, y = deg2num(coordinates[0], coordinates[1], zoomfaktor.value)
        url = 'http://a.tile.openstreetmap.org/{}/{}/{}.png'.format(zoomfaktor.value, x, y)
        return url
    return deg2num, get_osm_image, math


@app.cell
def __(get_osm_image, json_data, mo):
    #mo.md('Extrahiere die Geo-Koordinaten aus der Server-Antwort und hole ein Bild aus der OpenStreetMap.')
    image = get_osm_image(json_data['loc'].split(','))

    mo.image(src=image, alt="Kartenausschnitt von OpenStreetMap", width=400, height=400, rounded=True)

    return image,


if __name__ == "__main__":
    app.run()
