#!/usr/bin/env python
"""
Drop outliers and fixes datetime data type.
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def preprocessing(data, args):
    """
    Perform preprocessing on the input DataFrame.

    Parameters:
    - data: pandas DataFrame
        The input data that needs to be preprocessed.
    - args: argparse.Namespace
        An object containing parameters for the preprocessing.

    Returns:
    pandas DataFrame
        The preprocessed DataFrame with filtered rows and converted datetime column.
    """
    min_price = args.min_price
    max_price = args.max_price
    data = data.query(f"{min_price} <= price <= {max_price}").copy()
    data["last_review"] = pd.to_datetime(data['last_review'])

    return data


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading raw data...")
    data = pd.read_csv(artifact_local_path)
    logger.info("Preprocessing data...")
    data = preprocessing(data, args)
    logger.info("Saving preprocessed data...")
    data.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The name of the raw data file artifact in W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output file",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Output artifact description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price value to keep in the data",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price value to keep in the data",
        required=True
    )


    args = parser.parse_args()

    go(args)
