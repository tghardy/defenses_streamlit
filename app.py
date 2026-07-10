import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("df_streamlit.csv", index_col=0)


nonmodels = ['proposition', 'policy_trial', 'gold_label', 'proportion_right', 'PHATE_1', "PHATE_2", 'gini']
defenses = [d for d in df.columns if d not in nonmodels]

with st.sidebar:
    color_by = st.selectbox("Color plot by...", options=df.columns.drop("proposition"), index=14)

    props = st.selectbox("Include propositions that are...", options=["True", "False", "Both"], index=2)
    policies = st.selectbox("Include propositions with...", options=["Policies", "No policies", "Both"], index=2)

    st.write("Include the following defenses:")
    models = [
    col for col in defenses 
    if st.checkbox(col, value=True)
    ]

    if props == "True":
        df = df[df["gold_label"]==True]
    elif props == "False":
        df = df[df['gold_label']==False]

    if policies == "Policies":
        df = df[df['policy_trial'] == True]
    elif policies == "No policies":
        df = df[df['policy_trial'] == False]

df = df[models + nonmodels]

## Scoring code

features = defenses
p = features.mean(axis=1)

df['proportion_right'] = features.eq(df['gold_label'], axis=0).mean(axis=1)
df['gini'] = 1-(p**2+(1-p)**2)

### End scoring code


fig = px.scatter(data_frame=df, x="PHATE_1", y="PHATE_2", color=color_by, hover_data=["proposition", "gold_label", "policy_trial", 'proportion_right', 'gini'], color_discrete_sequence=px.colors.qualitative.Vivid, color_continuous_scale=px.colors.sequential.Viridis)
event = st.plotly_chart(fig, on_select="rerun")


selected_indices = event.selection.get("point_indices", [])    

if selected_indices:
    st.dataframe(df.iloc[selected_indices])

else:
    st.write("Select a point to view model selections")
