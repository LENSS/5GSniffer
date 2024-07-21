import argparse
import toml

def create_config(file_path, sample_rate, frequency, ssb_numerology, coreset_id, subcarrier_offset, num_prbs, numerology, dci_sizes_list, scrambling_id_start, scrambling_id_end, rnti_start, rnti_end, coreset_interleaving_pattern, coreset_reg_bundle_size, coreset_interleaver_size, coreset_nshift, coreset_duration):
    data = {
        "sniffer": {
            "file_path": file_path,
            "sample_rate": sample_rate,
            "frequency": frequency,
            "ssb_numerology": ssb_numerology,
        },
        "pdcch": [
            {
                "coreset_id": coreset_id,
                "subcarrier_offset": subcarrier_offset,
                "num_prbs": num_prbs,
                "numerology": numerology,
                "dci_sizes_list": dci_sizes_list,
                "scrambling_id_start": scrambling_id_start,
                "scrambling_id_end": scrambling_id_end,
                "rnti_start": rnti_start,
                "rnti_end": rnti_end,
                "coreset_interleaving_pattern": coreset_interleaving_pattern,
                "coreset_reg_bundle_size": coreset_reg_bundle_size,
                "coreset_interleaver_size": coreset_interleaver_size,
                "coreset_nshift": coreset_nshift,
                "coreset_duration": coreset_duration,
                "coreset_ofdm_symbol_start": 1,
                "AL_corr_thresholds": [1, 0.1, 0.1, 0.1, 1],
                "num_candidates_per_AL": [0, 3, 2, 2, 0],
            },
            {
                "coreset_id": coreset_id,
                "subcarrier_offset": subcarrier_offset,
                "num_prbs": num_prbs,
                "numerology": numerology,
                "dci_sizes_list": dci_sizes_list,
                "scrambling_id_start": scrambling_id_start,
                "scrambling_id_end": scrambling_id_end,
                "rnti_start": rnti_start,
                "rnti_end": rnti_end,
                "coreset_interleaving_pattern": coreset_interleaving_pattern,
                "coreset_reg_bundle_size": coreset_reg_bundle_size,
                "coreset_interleaver_size": coreset_interleaver_size,
                "coreset_nshift": coreset_nshift,
                "coreset_duration": coreset_duration,
                "coreset_ofdm_symbol_start": 0,
                "AL_corr_thresholds": [1, 0.1, 0.1, 0.1, 1],
                "num_candidates_per_AL": [0, 2, 2, 2, 0],
            },
            {
                "coreset_id": coreset_id,
                "subcarrier_offset": subcarrier_offset,
                "num_prbs": num_prbs,
                "numerology": numerology,
                "dci_sizes_list": dci_sizes_list,
                "scrambling_id_start": scrambling_id_start,
                "scrambling_id_end": scrambling_id_end,
                "rnti_start": rnti_start,
                "rnti_end": rnti_end,
                "coreset_interleaving_pattern": coreset_interleaving_pattern,
                "coreset_reg_bundle_size": coreset_reg_bundle_size,
                "coreset_interleaver_size": coreset_interleaver_size,
                "coreset_nshift": coreset_nshift,
                "coreset_duration": coreset_duration,
                "coreset_ofdm_symbol_start": 0,
                "AL_corr_thresholds": [1, 0.1, 0.1, 0.1, 1],
                "num_candidates_per_AL": [0, 3, 3, 2, 0],
            },
            {
                "coreset_id": coreset_id,
                "subcarrier_offset": subcarrier_offset,
                "num_prbs": num_prbs,
                "numerology": numerology,
                "dci_sizes_list": dci_sizes_list,
                "scrambling_id_start": scrambling_id_start,
                "scrambling_id_end": scrambling_id_end,
                "rnti_start": rnti_start,
                "rnti_end": rnti_end,
                "coreset_interleaving_pattern": coreset_interleaving_pattern,
                "coreset_reg_bundle_size": coreset_reg_bundle_size,
                "coreset_interleaver_size": coreset_interleaver_size,
                "coreset_nshift": coreset_nshift,
                "coreset_duration": coreset_duration,
                "coreset_ofdm_symbol_start": 1,
                "AL_corr_thresholds": [1, 1, 0.1, 0.1, 1],
                "num_candidates_per_AL": [0, 0, 1, 1, 0],
            }
        ]
    }

    with open("config.toml", "w") as toml_file:
        toml.dump(data, toml_file)

    print("TOML file generated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a TOML configuration file.")
    parser.add_argument("--rnti_start", type=int, required=True, help="Start value of RNTI.")
    parser.add_argument("--rnti_end", type=int, required=True, help="End value of RNTI.")
    parser.add_argument("--scrambling_id_start", type=int, required=True, help="Start value of scrambling id.")
    parser.add_argument("--scrambling_id_end", type=int, required=True, help="End value of scrambling id.")

    args = parser.parse_args()

    create_config(
        file_path="/tmp/n71.fc32",
        sample_rate=23040000,
        frequency=626450000,
        ssb_numerology=0,
        coreset_id=4,
        subcarrier_offset=-310,
        num_prbs=96,
        numerology=0,
        dci_sizes_list=[40, 49],
        scrambling_id_start=args.scrambling_id_start,
        scrambling_id_end=args.scrambling_id_end,
        rnti_start=args.rnti_start,
        rnti_end=args.rnti_end,
        coreset_interleaving_pattern="interleaved",
        coreset_reg_bundle_size=2,
        coreset_interleaver_size=3,
        coreset_nshift=123,
        coreset_duration=1
    )
