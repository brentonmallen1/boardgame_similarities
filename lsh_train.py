'''
This script is used to build the LSH model
'''

''' TODO Need to be able to rebuild this from scratch for repeatability and
feature editing
'''

import utils as _utils
from datasketch import MinHashLSHForest
from sklearn.externals import joblib
# ^ only needed because that's how I stored originally
import pickle
import argparse



def build_lsh_forest_hash(game_data):
    forest = MinHashLSHForest(num_perm=_utils.HASH_REZ)
    for ind, row in game_data.iterrows():
        try:
            forest.add(f"{row['title']} (id:{row['id']})", row['_sim_hash'])
        except ValueError:
            print(f"{row['title']} already added")
        except:
            raise
    forest.index()
    return forest


def train_lsh_forest(data_file,
                     save_name=DEFAULT_SAVENAME
                     ):
    # load the game data from the gzip file
    print(f'Loading data from {data_file}...')
    game_data = joblib.load(data_file)
    print('Data Loaded!')

    # extract the fields into a list to generate hash
    print('Generating similarity tokens...')
    game_data['_sim_tokens'] = game_data[_utils.SIMILARITY_FIELDS].apply(
        lambda row: _utils.process_tokens(row), axis=1)
    print('Similarity tokens generated!')

    print('Generating similarity hashes...')
    game_data['_sim_hash'] = game_data['_sim_tokens'].apply(
        lambda x: _utils.compute_sim_hash(x))
    print('Similarity hashes generated!')

    print('Building LSH forest...')
    lsh_forest = build_lsh_forest_hash(game_data)
    print('LSH forest planted!')

    print(f'Saving forest to {save_name}')
    with open(save_name, 'wb') as f:
        pickle.dump(lsh_forest, f, protocol=4)
    print("LSH Forest Saved!")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        default=_utils.LSH_SAVENAME,
                        help="filename to save trained hash forest")
    parser.add_argument("-d",
                        "--data",
                        help="game data file to turn into a hash forest")
    args = parser.parse_args()
    print("Starting LSH forest training...")
    train_lsh_forest(args.data, save_name=args.file)
    print("LSH forest training complete!")
