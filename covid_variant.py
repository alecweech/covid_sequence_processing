class covid_variant:
    def __init__(self, reference_genome, individual_seq, seq_dates = None, seq_counts = None):
        self.reference_genome = reference_genome
        self.individual_seq = individual_seq
        self.nucleotide_variants = None
        self.protein_sequences = None
