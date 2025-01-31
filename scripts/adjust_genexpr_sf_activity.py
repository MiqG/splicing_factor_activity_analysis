import argparse
import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np

# variables
SAVE_PARAMS = {"sep": "\t", "index": False, "compression": "gzip"}

##### FUNCTIONS #####
class FClayer(nn.Module):
    def __init__(self, input_size, output_size):
        super(FClayer, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        x = self.fc(x)
        return x

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activity_file", type=str)
    parser.add_argument("--models_dir", type=str)
    parser.add_argument("--output_file", type=str)

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    activity_file = args.activity_file
    models_dir = args.models_dir
    output_file = args.output_file

    # load
    activity = pd.read_table(activity_file, index_col=0)
    weights = [torch.load(os.path.join(models_dir,f), weights_only=True) for f in os.listdir(models_dir) if "weights" in f]
    input_regulators = list(pd.read_table(os.path.join(models_dir,"input_regulators.tsv.gz"), header=None)[0])
    output_regulators = list(pd.read_table(os.path.join(models_dir,"output_regulators.tsv.gz"), header=None)[0])

    # prep data
    activity = pd.merge(
        pd.DataFrame(index=input_regulators),
        activity,
        how="left", left_index=True, right_index=True
    )
    X = torch.tensor(activity.fillna(0).T.values, dtype=torch.float32)

    model = FClayer(input_size=len(input_regulators), output_size=len(output_regulators))

    activity_preds = []
    for k in range(len(weights)):
        model.load_state_dict(weights[k])        
        # make predictions
        model.eval()
        with torch.no_grad():
            Y_hat = model(X)

        # prep outputs
        activity_pred = pd.DataFrame(Y_hat.detach().numpy().T, index=output_regulators, columns=activity.columns)
        activity_pred.index.name = "regulator"
        
        activity_preds.append(activity_pred)
        
    # average predictions
    activity_stack = np.stack([df.values for df in activity_preds])
    activity_avg = np.mean(activity_stack, axis=0)
    activity_preds = pd.DataFrame(
        activity_avg, index=activity_preds[0].index, columns=activity_preds[0].columns
    )
    
    # save
    activity_preds.reset_index().to_csv(output_file, **SAVE_PARAMS)


##### SCRIPT #####
if __name__ == "__main__":
    main()
    print("Done!")