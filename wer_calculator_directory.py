##########################################################################################################################
# Script: wer_calculator_directory.py
#
# Description:
# This Python script calculates the Word Error Rate (WER) using the `werpy` library (Armstrong 2024) for transcript pairs 
# located in a specified directory. It is designed to compare original reference transcripts (e.g. ICE_NIG_bdis_01.txt) 
# with corresponding ASR-generated transcriptions (e.g. ICE_NIG_bdis_01_whisper.txt).
#
# The script performs the following steps:
# 1. Identifies all reference transcripts and matches them with their corresponding ASR transcriptions.
# 2. Normalizes both reference and hypothesis transcripts using `werpy.normalize()`.
# 3. Calculates the WER for each pair using `werpy.wer()`.
# 4. Counts the number of words in each normalized transcript.
# 5. Aggregates all results into a single CSV file (`wer_results_werpy.csv`) for further analysis.
#
# This script is distributed under the GNU General Public License.
# Copyright 21/07/2025 by Andreas Weilinghoff.
# You may use/modify this script as you wish. It would just be nice if you cite me:
# Weilinghoff, A. (2025): wer_calculator_directory.py (Version 1.0) [Source code]. https://www.andreas-weilinghoff.com/#code
##########################################################################################################################

# Load libraries
import os
import pandas as pd
import werpy

# Set the directory containing your files
directory = "C:\\input directory where transcriptions are saved"

# Prepare to collect results
results = []

# List all files in the directory
files = os.listdir(directory)

# Filter out the reference files and create pairs with hypothesis files
reference_files = [f for f in files if "_whisper" not in f]

for ref_file in reference_files:
    ref_path = os.path.join(directory, ref_file)
    # Read the reference file
    with open(ref_path, 'r', encoding='utf-8') as file:
        reference_text = file.read()

    # Normalize the reference text
    normalized_ref_text = werpy.normalize(reference_text)
    
    # Count words in the normalized reference text
    reference_word_count = len(normalized_ref_text.split())

    # Find and process all corresponding hypothesis files
    prefix = ref_file[:-4]  # Remove ".txt" from reference file name
    hypothesis_files = [f for f in files if f.startswith(prefix) and "_whisper" in f]
    
    for hyp_file in hypothesis_files:
        hyp_path = os.path.join(directory, hyp_file)
        with open(hyp_path, 'r', encoding='utf-8') as file:
            hypothesis_text = file.read()

        # Normalize the hypothesis text
        normalized_hyp_text = werpy.normalize(hypothesis_text)

        # Count words in the normalized hypothesis text
        ASR_word_count = len(normalized_hyp_text.split())

        # Compute WER
        error_rate = werpy.wer(normalized_ref_text, normalized_hyp_text)
        
        # Save the result
        results.append({
            "Reference File": ref_file,
            "Hypothesis File": hyp_file,
            "Word Error Rate": error_rate,
            "reference_word_count": reference_word_count,
            "ASR_word_count": ASR_word_count
        })

# Create a DataFrame
df = pd.DataFrame(results)

# Save the results to a CSV file
csv_path = os.path.join(directory, "wer_results_werpy.csv")
df.to_csv(csv_path, index=False)

print("WER calculations complete. Results saved to 'wer_results_werpy.csv'.")
