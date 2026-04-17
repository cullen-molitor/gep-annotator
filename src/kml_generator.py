import os
import tempfile
from pathlib import Path

from config import (
    BUFFER_SIZE_DEGREES,
    LOOKAT_RANGE_METERS,
    REFRESH_INTERVAL_SECONDS,
    TARGET_DATE,
    TARGET_KML_PATH,
    WATCHER_KML_PATH,
)


def generate_target_kml(location_id: str, lat: float, lon: float) -> str:
    name = f"{location_id}_2020"
    buffer = BUFFER_SIZE_DEGREES

    min_lon = lon - buffer
    max_lon = lon + buffer
    min_lat = lat - buffer
    max_lat = lat + buffer

    bbox_coords = (
        f"{min_lon},{min_lat},0 "
        f"{max_lon},{min_lat},0 "
        f"{max_lon},{max_lat},0 "
        f"{min_lon},{max_lat},0 "
        f"{min_lon},{min_lat},0"
    )

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
<Document>
  <name>{name}</name>

  <Style id="bbox_style">
    <LineStyle>
      <color>ff0000ff</color>
      <width>2</width>
    </LineStyle>
    <PolyStyle>
      <fill>0</fill>
    </PolyStyle>
  </Style>

  <Placemark>
    <name>{location_id}</name>
    <description>Bounding box: {buffer} degree buffer</description>
    <LookAt>
      <gx:TimeStamp><when>{TARGET_DATE}</when></gx:TimeStamp>
      <gx:ViewerOptions>
        <gx:option name="historicalimagery" enabled="1" />
        <gx:option enabled="0" name="sunlight" />
        <gx:option enabled="0" name="streetview" />
      </gx:ViewerOptions>
      <longitude>{lon}</longitude>
      <latitude>{lat}</latitude>
      <altitude>0</altitude>
      <heading>0</heading>
      <tilt>0</tilt>
      <range>{LOOKAT_RANGE_METERS}</range>
      <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
    </LookAt>
    <styleUrl>#bbox_style</styleUrl>
    <Polygon>
      <outerBoundaryIs>
        <LinearRing>
          <coordinates>{bbox_coords}</coordinates>
        </LinearRing>
      </outerBoundaryIs>
    </Polygon>
  </Placemark>
</Document>
</kml>"""


def generate_watcher_kml() -> str:
    target_href = f"file://{TARGET_KML_PATH.resolve()}"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <NetworkLink>
    <name>ASM Annotator Target</name>
    <flyToView>1</flyToView>
    <Link>
      <href>{target_href}</href>
      <refreshMode>onInterval</refreshMode>
      <refreshInterval>{REFRESH_INTERVAL_SECONDS}</refreshInterval>
    </Link>
  </NetworkLink>
</Document>
</kml>"""


def write_target_kml(content: str) -> None:
    fd, tmp_path = tempfile.mkstemp(dir=TARGET_KML_PATH.parent, suffix=".kml")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp_path, TARGET_KML_PATH)
    except BaseException:
        os.unlink(tmp_path)
        raise


def write_watcher_kml() -> None:
    with open(WATCHER_KML_PATH, "w") as f:
        f.write(generate_watcher_kml())
