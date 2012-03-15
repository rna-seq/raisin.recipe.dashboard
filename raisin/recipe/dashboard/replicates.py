from raisin.recipe.dashboard.cube import Cube


class Renderer:

    def __init__(self, output):
        """
        Store the output to render to
        """
        self.output = output

    def render(self, header, replicate, afile, number):
        """
        Render the cell depending on the header
        """
        if header == "file_location":
            html = self.file_location(header, replicate, afile, number)
        elif header in ["genome_version"]:
            html = self.genome_version(afile)
        elif header in ["annotation_version"]:
            html = self.annotation_version(afile)
        else:
            html = self.header(header, afile)
        self.output.write(html)

    def file_location(self, header, replicate, afile, number):
        """
        Render the file location
        """
        if len(replicate[1]) == 1:
            view = "Raw data"
        else:
            if afile['type'] == 'fastq':
                view = 'FastqRd%d' % number
            elif afile['type'] == 'fasta':
                view = 'FastaRd%d' % number
            elif afile['type'] == 'bam':
                view = 'BAM%d' % number
            else:
                print replicate
                raise AttributeError
        template = """<td><a href="%s">%s</a></td>\n"""
        return template % (afile[header], view)

    def genome_version(self, afile):
        """
        Render the genome version
        """
        template = ("""<td><a href="%s" title="%s">"""
                    """%s</a></td>\n""")
        return template % (afile["genome_url"],
                           afile["genome"],
                           afile["genome_version"])

    def annotation_version(self, afile):
        """
        Render the annotation version
        """
        template = ("""<td><a href="%s" title="%s">"""
                    """%s</a></td>\n""")
        return template % (afile["annotation_url"],
                           afile["annotation"],
                           afile["annotation_version"])

    def header(self, header, afile):
        """
        Render the header
        """
        return "<td>%s</td>\n" % afile[header]


class Replicates(Cube):
    """
    Replicates cube
    """

    def __init__(self, accessions, rows, cols):
        """
        Keep the accessions for the replicates
        """
        self.replicates = {}
        Cube.__init__(self, accessions, rows, cols)

    def add_accession_files(self, files, accession_id, rows_key, cols_key):
        """
        Add accession files
        """
        Cube.add_accession_files(self, files, accession_id, rows_key, cols_key)
        key = (tuple(rows_key), tuple(cols_key))
        if key in self.replicates:
            self.replicates[key].append((accession_id, files))
        else:
            self.replicates[key] = [(accession_id, files)]

    def produce_table(self, output, key, attribute_categories):
        """
        Produce the table
        """
        replicates = self.replicates[key]

        remove = self.dimensions
        for key, value in attribute_categories.items():
            if value == "":
                remove.append(key)
        # Remove attribute with only one possible value
        #    elif len(self.attributes[key]) == 1:
        #        remove.append(key)
        headers = []
        for key in replicates[0][1][0].keys():
            if not key in remove:
                headers.append(key)

        output.write("<table>\n")
        output.write("<tr>\n")
        for key in headers:
            output.write("<th>%s</th>\n" % key)
        output.write("</tr>\n")

        renderer = Renderer(output)

        for replicate in replicates:
            number = 0
            for afile in replicate[1]:
                number += 1
                output.write("<tr>\n")
                for header in headers:
                    renderer.render(header, replicate, afile, number)
                output.write("</tr>\n")

        output.write("</table>\n")
