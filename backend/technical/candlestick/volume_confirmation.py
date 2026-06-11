def calculate_volume_factor(
    records,
):

    if len(records) < 20:
        return 1.0

    volumes = [
        float(record.volume)
        for record in records
    ]

    latest_volume = volumes[0]

    average_volume = (
        sum(volumes[1:20])
        / 19
    )

    if average_volume == 0:
        return 1.0

    return (
        latest_volume
        / average_volume
    )