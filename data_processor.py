class DataProcessor():
    def __init__(self):
        pass

    def data_cleaner(self, data):
        """Get data from file importer, make it feasible."""

        # Delete line beginnings
        data = [line[2:] for line in data]

        # Partnumber is always the first line
        partnumber = data[0]

        # Find where header ends
        header_end_line = [line for line in data if "omment" in line][0]
        self.header_end_index = data.index(header_end_line) - 1

        # Split data to header and other unclean data
        unclean_header = data[1:self.header_end_index]
        unclean_body = data[self.header_end_index:]

        header = self.header_cleaner(unclean_header)
        body = self.body_cleaner(unclean_body, header)

        data = body
        data.insert(0, header)
        return partnumber, data

    def header_cleaner(self, header):
        """Clean up header."""

        for idx, item in enumerate(header):
            if ("  ") in item:  # Delete multiple whitespaces
                header[idx] = item[:item.index("  ")]
            if "[" in item:  # Delete limits
                header[idx] = item[:item.index("[")-1]
        # Delete unused column
        header = [
            item for item in header if "Software Status" not in item
            ]
        return header

    def body_cleaner(self, body, header):
        """Clean up body."""

        # Delete useless data
        body = [line.split() for line in body if len(line) > 200]
        # Delete useless lines
        body = [line for line in body if "Fluegel" not in line]

        # If clip separation is necessary
        if "clip" in header[-1].lower() and len(body[0][-1]) > 1:
            for idx, line in enumerate(body):
                separated_clips = list(line[-1])
                body[idx] = line[:-1] + separated_clips
        return body
