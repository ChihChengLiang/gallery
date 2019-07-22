from gallery import config
import matplotlib.pyplot as plt
import json
import pandas as pd
import requests
import seaborn as sns
sns.set()

DATA_URL = "https://raw.githubusercontent.com/PDIS/quadratic-voting-frontend/master/data/ProposalPolls.json"


def load_json(url):
    response = requests.get(DATA_URL)
    # The data has a weird first few bytes
    return pd.read_json(response.content[3:])


polls = load_json(DATA_URL)

n_proposal_voted = (
    polls[['UserID', 'Count']]
    .groupby('UserID')
    .count()
    .rename(columns={'Count': 'n_proposal_voted'})
)
User_cost = (
    polls[['UserID', 'Count']]
    .groupby('UserID')
    .apply(lambda x: x['Count']**2)
    .groupby('UserID')
    .sum()
    .to_frame(name='Cost')
)

user_features = User_cost.merge(
    n_proposal_voted, left_index=True, right_index=True)

cost_summary = (
    user_features[['n_proposal_voted', 'Cost']]
    .groupby(['n_proposal_voted', 'Cost'])
    .size()
    .rename('users')
    .to_frame()
    .reset_index()
)

sns.scatterplot(
    x=cost_summary.n_proposal_voted,
    y=cost_summary.Cost,
    size=cost_summary.users,
    sizes=(30, 200),
)
plt.xlabel("Number of Proposals Voted")
plt.ylabel("Cost Spent")
plt.title(
    f"How {polls.UserID.nunique()} Users vote in Quadratic-Voting Experiment of PDIS Hackthon")
plt.savefig('qv.png')
