class covid_variant:
    def __init__(self, reference_genome, individual_seq):
        self.reference_genome = reference_genome
        self.individual_seq = individual_seq
        self.nucleotide_variants = None
        self.protein_sequences = None