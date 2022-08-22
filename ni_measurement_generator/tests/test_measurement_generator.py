"""Tests to validate the python measurement generator."""
import pathlib

import pytest
from ni_measurement_generator import template


generator_path = pathlib.Path(template.__file__).parent


def test___command_line_args___create_measurement___render_without_exception(tmpdir):
    """Given example command line args when create_measurement assert renders without exceptions."""
    temp_directory = pathlib.Path(tmpdir.mkdir("measurement_files"))

    with pytest.raises(SystemExit):
        template.create_measurement(
            [
                "SampleMeasurement",
                "1.0.0.0",
                "Measurement",
                "Product",
                "--ui-file",
                "MeasurementUI.measui",
                "--service-class",
                "SampleMeasurement_Python",
                "--service-id",
                "{E0095551-CB4B-4352-B65B-4280973694B2}",
                "--description",
                "description",
                "--directory-out",
                temp_directory,
            ]
        )

    golden_path = generator_path / "example_renders"

    _assert_equal(
        golden_path / "example.py",
        temp_directory / "measurement.py",
    )
    _assert_equal(
        golden_path / "example.serviceconfig",
        temp_directory / "SampleMeasurement.serviceconfig",
    )
    _assert_equal(
        golden_path / "example.bat",
        temp_directory / "start.bat",
    )


def _assert_equal(expected_path: pathlib.Path, result_path: pathlib.Path):
    expected = expected_path.read_text()
    result = result_path.read_text()

    assert expected == result