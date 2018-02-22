#!/usr/bin/env python
import argparse

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"


class GG_Taxa:

    """ A greengenes taxa object"""
    def clean_taxastr(self, taxastr):
        # Get the taxa and strip headers
        taxa_list = [taxa.lstrip(self.TAXA_PREFIX[level]) for level, taxa in enumerate(taxastr.split(';'))]
        # Make sure it is length 7
        taxa_list = taxa_list + (7 - len(taxa_list)) * ['']
        return taxa_list

    def __init__(self, node, taxastr, score):
        self.TAXA_PREFIX = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
        self.node = node
        self.taxastr = taxastr
        self.score = score
        self.taxalist = self.clean_taxastr(self.taxastr)

    @property
    def get_taxalist(self):
        return self.taxalist

    def set_taxa(self, level, taxa):
        tlist = self.get_taxalist
        tlist[level - 1] = taxa
        self.taxalist = tlist

    @property
    def formatted_taxastr(self):
        return ';'.join([''.join(taxatuple) for taxatuple in zip(self.TAXA_PREFIX, self.taxalist)])

    @property
    def get_k(self):
        return self.taxalist[0]

    @property
    def get_p(self):
        return self.taxalist[1]

    @property
    def get_c(self):
        return self.taxalist[2]

    @property
    def get_o(self):
        return self.taxalist[3]

    @property
    def get_f(self):
        return self.taxalist[4]

    @property
    def get_g(self):
        return self.taxalist[5]

    @property
    def get_s(self):
        return self.taxalist[6]


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='<This is what the script does>')

    # Pecan file
    parser.add_argument('-p', '--pecan', dest='pecan', help='The pecan file')
    # GG file
    parser.add_argument('-g', '--greengenes', dest='greengenes', help='The greengenes file')
    # Output file
    parser.add_argument('-o', '--outfile', dest='outfile', help='The output file')

    # Parse arguments
    args = parser.parse_args()
    pecan = args.pecan
    greengenes = args.greengenes
    outfile = args.outfile

    TAXA_STARTERS = ("d_", "p_", "c_", "o_", "f_", "g_")

    # Read the greengenes assigned to a dict of GG Objects
    gg_dict = {}
    with open(greengenes, 'r') as greengenes_h:
        for line in greengenes_h:
            node, taxa, score = line.rstrip('\n').split('\t')
            gg_dict[node] = GG_Taxa(node, taxa, score)

    # Munge pecan to just genus_species combos
    with open(pecan, 'r') as pecan_h:
        for line in pecan_h:
            node, taxa, score = line.rstrip('\n').split('\t')
            # We only want genus/species combos
            if not taxa.startswith(TAXA_STARTERS):
                print "Node: {}".format(node)
                try:
                    genus, species = taxa.split('_', 1)
                except ValueError:
                    genus = taxa
                    species = taxa

                print "\tPecan:\t{}\t{}".format(genus, species)
                # GG Lookup
                gg = gg_dict[node]
                print "\tGreenGenes:\t{}\t{}".format(gg.get_g, gg.get_s)
                if genus in gg.get_g:
                    print "\t\tGenus Match"
                else:
                    print "\t\tGenus Mismatch"
                    gg.set_taxa(6, genus)
                if species in gg.get_s:
                    print "\t\tSpecies Match"
                else:
                    print "\t\tSpecies Mismatch"
                    gg.set_taxa(7, species)

    # Write output
    with open(outfile, 'w') as outfile_h:
        for node in gg_dict:
            gg = gg_dict[node]
            outfile_h.write("{}\t{}\t{}\n".format(node, gg.formatted_taxastr, gg.score))



if __name__ == '__main__':
    main()
