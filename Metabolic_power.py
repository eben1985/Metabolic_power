import pandas as pd 
import os
import numpy as np
import streamlit as st
import plotly.express as px

def savoia_formula(velocity, accel):
    ans = (30.4*np.power(np.tan(np.radians(90-np.degrees(np.arctan(9.8/accel)))),4)-5.0975*np.power(np.tan(np.radians(90-np.degrees(np.arctan(9.8/accel)))),3)+46.3*np.power(np.tan(np.radians(90-np.degrees(np.arctan(9.8/accel)))),2)+17.696*np.tan(np.radians(90-np.degrees(np.arctan(9.8/accel))))+4.66)*(np.sqrt((9.8*9.8)+(accel*accel))/9.8)*velocity+0.4*velocity*velocity*0.0225
    return ans

# data_frames = []
# columns_to_drop = ['Odometer', 'Latitude', 'Longitude', 'Heart Rate', 'Player Load', 'Positional Quality (%)', 'HDOP', '#Sats']


# folder_path = 'C:/Users/eben.opperman/Desktop/Metabolic_Power'  # replace with your folder path
# file_list = os.listdir(folder_path)

# for file in file_list:
#     if file.endswith('.csv'):
#         if file.endswith('.csv'):
#             file_path = os.path.join(folder_path, file)
#             df = pd.read_csv(file_path, skiprows=8, header=0)
            
#             filename = os.path.basename(file_path)
#             filename = filename.replace('.csv', '')
#             session_name, rest = filename.split(' Export for ')
#             name, unit_id = rest.rsplit(' ', 1)
#             df.insert(0, 'Session Name', session_name)
#             df.insert(1, 'Name', name)
#             df.insert(2, 'Unit ID', unit_id)
#             df = df[df['Velocity'] >= 1]
#             df['Savoia'] = df.apply(lambda row: savoia_formula(row['Velocity'], row['Acceleration']), axis=1)
#             data_frames.append(df)

# # Concatenate all DataFrames into one
# result_df = pd.concat(data_frames, ignore_index=True)
# result_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# # Save the concatenated DataFrame to a new CSV file
# result_file_path = f'{session_name}_concatenated_metabolic_data.csv'
# result_df.to_csv(result_file_path, index=False)

def main():
    st.set_page_config(layout='wide')
    st.title('Metabolic Power Analysis')

    uploaded_files = st.file_uploader("Select all CSV files", type=["csv"], accept_multiple_files=True)

    if uploaded_files is not None:

        with st.spinner('Calculating Savoia algorithm for all athletes...'):

            data_frames = []
            columns_to_drop = ['Odometer', 'Latitude', 'Longitude', 'Heart Rate', 'Player Load', 'Positional Quality (%)', 'HDOP', '#Sats']

            for uploaded_file in uploaded_files:
                # if uploaded_file.endswith('.csv'):
                file_name = uploaded_file.name
                df = pd.read_csv(uploaded_file, skiprows=8, header=0)

                file_name = file_name.replace('.csv', '')
                session_name, rest = file_name.split(' Export for ')
                name, unit_id = rest.rsplit(' ', 1)
                df.insert(0, 'Session Name', session_name)
                df.insert(1, 'Athlete', name)
                df.insert(2, 'Unit ID', unit_id)
                df = df[df['Velocity'] >= 1]
                df['Savoia'] = df.apply(lambda row: savoia_formula(row['Velocity'], row['Acceleration']), axis=1)
                data_frames.append(df)

            if len(data_frames) > 0:
                # Concatenate all DataFrames into one
                result_df = pd.concat(data_frames, ignore_index=True)
                result_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

                # Display the concatenated DataFrame
                st.subheader('Concatenated Report:')
                with st.expander("Open to view concatenated data:"):
                    st.dataframe(result_df)

                fig = px.line(result_df, x='Seconds', y='Savoia', color='Athlete', title='Savoia Time Graph for session (Velocity >1)')
                st.plotly_chart(fig, use_container_width=True)

                grouped_df_max = result_df.groupby('Athlete')[['Acceleration', 'Velocity', 'Savoia']].agg('max').reset_index()
                st.subheader("Maximums")
                with st.expander("Open to see maximums:"):
                    st.table(grouped_df_max)


                # Save the concatenated DataFrame to a new CSV file
                output_filename = f'{session_name}_concatenated_metabolic_data.csv'

                result_df_csv = result_df.to_csv(index=False)

                st.download_button(
                    label = "Download data CSV", 
                    data=result_df_csv, 
                    file_name=output_filename,
                    mime="text/csv"
                    )
    else:
        st.info("Please upload files.")


if __name__ == "__main__":
    main()