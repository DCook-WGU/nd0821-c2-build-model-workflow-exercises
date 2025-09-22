#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="exercise_5", job_type="process_data")

    ## YOUR CODE HERE
    #pass

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    # opening with pandes
    logger.info("Opening artifact with panads")
    df = pd.read_parquet(artifact.file()) 


    # drop duplicates
    logger.info("Dropping duplicates")
    df = df.drop_duplicates().reset_index(drop=True)

    #feature engineering

    logger.info("fixing null values on title column")
    # Correcting title column null values. filling with empty string
    df['title'].fillna(value='', inplace=True)

    logger.info("fixing null values on song_name column")
    # Correcting song_name column null values. filling with empty string
    df['song_name'].fillna(value='', inplace=True)

    logger.info("creating new column/feature called 'text_feature'")
    # creating new feature, concatting the title and song name together
    df['text_feature'] = df['title'] + ' ' + df['song_name']

    # Saving preprocessed dataset to a new file, csv

    # Assigning the file name
    filename = 'preprocessed_data.csv'

    # saving file
    df.to_csv(filename)

    # creating a new artifact
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description,
    )

    # adding our file to the artifact
    artifact.add_file(filename)

    logger.info("logging artifact")
    run.log_artifact(artifact)

    # deleting file from os
    os.remove(filename)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
