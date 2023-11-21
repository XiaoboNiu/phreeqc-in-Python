# phreeqc-in-Python
Python-written best 〖Log〗_k fitting code template

The following Python-IPhreeqcCOM template code simplifies the search for the best fitting 〖Log〗_k values between the results obtained from Phreeqc and experimental data. The search is automated using the least squares method, which gradually narrows down the range of values based on the parameters provided.

Initially, the experimental data is imported into the process, and the 〖Log〗_k value is determined based on the provided boundary conditions. Next, the phreeqc module is utilized to calculate the leaching of SO42-. A range of Se initial concentration-SO42- leaching curves corresponding to different 〖Log〗_k values is obtained, and the closeness of these curves to the experimental data is evaluated using the Root Mean Squared Error (RMSE). The least squares method is then applied to determine the best-fitting 〖Log〗_k value within the given range, which corresponds to the smallest RMSE.
