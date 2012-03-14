from raisin.recipe.dashboard.cube import Cube

class Replicates(Cube):

    def __init__(self, accessions, rows, cols):
        self.replicates = {}
        Cube.__init__(self, accessions, rows, cols)

    def add_accession_files(self, accession_id, files, rows_key, cols_key):
        Cube.add_accession_files(self, accession_id, files, rows_key, cols_key)
        key = (tuple(rows_key), tuple(cols_key))
        if key in self.replicates:
            self.replicates[key].append((accession_id, files))
        else:
            self.replicates[key] = [(accession_id, files)]

    def produce_table(self, output, key, attribute_categories):
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

        for replicate in replicates:
            number = 0
            for file in replicate[1]:
                number += 1
                output.write("<tr>\n")
                for header in headers:
                    if header == "file_location":
                        if len(replicate[1]) == 1:
                            view = "Raw data"
                        else:
                            if file['type'] == 'fastq':
                                view = 'FastqRd%d' % number
                            elif file['type'] == 'fasta':
                                view = 'FastaRd%d' % number
                            elif file['type'] == 'bam':
                                view = 'BAM%d' % number
                            else:
                                print replicate
                                raise AttributeError
                        template = """<td><a href="%s">%s</a></td>\n"""
                        output.write(template % (file[header], view))
                    elif header in ["genome_version"]:
                        template = ("""<td><a href="%s" title="%s">"""
                                    """%s</a></td>\n""")
                        output.write(template % (file["genome_url"],
                                                 file["genome"],
                                                 file["genome_version"]))
                    elif header in ["annotation_version"]:
                        template = ("""<td><a href="%s" title="%s">"""
                                    """%s</a></td>\n""")
                        output.write(template % (file["annotation_url"],
                                                 file["annotation"],
                                                 file["annotation_version"]))
                    else:
                        output.write("<td>%s</td>\n" % file[header])
                output.write("</tr>\n")

        output.write("</table>\n")
