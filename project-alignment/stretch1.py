import sys
import alignment


def main():
    sequences = {}
    current_species = None
    with open("lct_exon8.txt") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                header_part = line.split()[0][1:]
                parts = header_part.split('_')
                current_species = parts[1]
                sequences[current_species] = ""
            elif current_species:
                sequences[current_species] += line

    unknown_seq = sequences.pop('unknown')
    suspect_list = sequences
    best_match_species = None
    lowest_score = float('inf')

    for species, species_seq in suspect_list.items():
        score, _, _ = alignment.align(species_seq, unknown_seq)
        print(f"Score for {species}: {score}")

        if score < lowest_score:
            lowest_score = score
            best_match_species = species
    species_map = {
        'hg38': 'Human - Homo sapiens',
        'panTro4': 'Chimp - Pan troglodytes',
        'rheMac3': 'Rhesus macque - Macaca mulatta',
        'canFam3': 'Dog - Canis lupus familiaris',
        'rn5': 'Rat - Rattus norvegicus',
        'mm10': 'Mouse - Mus musculus'
    }

    if best_match_species:
        culprit_name = species_map.get(best_match_species, "an unknown species")
        print(f"The unknown sample is most similar to: **{best_match_species}** ({culprit_name})")
        print(f"It had the lowest alignment score: **{lowest_score}**")
        print(f"\nConclusion: The hair fragment belongs to a **{culprit_name}**.")


if __name__ == '__main__':
    main()
