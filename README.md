# SeismicDataWorldwide

SeismicDataWorldwide is an open-source repository that provides a comprehensive collection of global earthquake data. The data, sourced from the USGS Earthquake Catalog, includes details of earthquakes with a magnitude of 4.5 and above, spanning from 2000 to 2024.

## Data Description

The dataset contains the following fields:

- `time`: The timestamp of the earthquake.
- `latitude`, `longitude`: The geographical coordinates of the earthquake's epicenter.
- `depth`: The depth of the earthquake in kilometers.
- `mag`: The magnitude of the earthquake.
- `magType`: The method or algorithm used to calculate the preferred magnitude of the earthquake.
- `nst`: The number of seismic stations that reported P- and S-arrival times for this earthquake.
- `gap`: The largest azimuthal gap between azimuthally adjacent stations (in degrees).
- `dmin`: The minimum distance to the source of the earthquake.
- `rms`: The root-mean-square (RMS) travel time residual, in sec, using all weights.
- `net`: The ID of a data contributor.
- `id`: A unique identifier for the earthquake.
- `updated`: Time when the event was most recently updated.
- `place`: Description of the location of the earthquake.
- `type`: Type of seismic event.
- `horizontalError`, `depthError`, `magError`, `magNst`: Error measurements.
- `status`: Status of the event (automatic or reviewed).
- `locationSource`, `magSource`: Source of location and magnitude data.

## Usage

This dataset can be used for various purposes such as earthquake prediction, geological research, understanding the distribution of earthquakes around the world, etc.

## Updates

The dataset will be updated regularly to include the most recent earthquake data from the USGS Earthquake Catalog.

## Contributing

Contributions are welcome. Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgements

This dataset is sourced from the USGS Earthquake Catalog. We are grateful to USGS for making this data publicly available.
