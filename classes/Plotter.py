import pandas as pd
import matplotlib.pyplot as plt
import os

class Plotter:
    def __init__(self, filename="log.csv"):
        self.filename = filename
        self.data = None
    
    def load_data(self):
        """Loads data from a CSV file."""
        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename)
            print(f"Data loaded from {self.filename}")
        else:
            raise FileNotFoundError(f"{self.filename} does not exist in the directory.")
    
    def plot_columns(self, columns=None, show=False):
        """Plots specified columns against the second column (assumed to be time). Each call generates a new figure."""
        if self.data is None:
            raise ValueError("Data not loaded. Use load_data() before plotting.")
        
        # Create a new figure for each plot_columns call
        plt.figure()

        # Assuming the second column is time
        time = self.data.iloc[:, 1]
        time_label = self.data.columns[1]
        
        # Handle case where no columns are specified (plot all except time)
        if columns is None:
            # If no columns are specified, plot all columns except the second one (time)
            columns = self.data.columns.drop(self.data.columns[1])  # All columns except the time column
        else:
            # Validate that all provided column names or numbers are valid
            valid_columns = []
            for col in columns:
                if isinstance(col, int) and col < len(self.data.columns):
                    # If column is specified by index, use it
                    valid_columns.append(self.data.columns[col])
                elif isinstance(col, str) and col in self.data.columns:
                    # If column is specified by title, use it
                    valid_columns.append(col)
                else:
                    print(f"Invalid column reference: {col}")
            
            columns = valid_columns
        
        # Concatenate the titles of the selected columns for the plot title and y-label
        concatenated_columns = ", ".join([col.replace("engine.", "") for col in columns])  # Remove 'engine.' prefix
        
        # Plot each column against the time column
        for column in columns:
            clean_column_name = column.replace("engine.", "")  # Remove 'engine.' prefix from column name
            plt.plot(time, self.data[column], label=clean_column_name)
        
        # Set plot labels and title
        plt.xlabel(time_label)
        plt.ylabel(f"Values of {concatenated_columns}")
        plt.legend()
        plt.title(f"Plot of {concatenated_columns} vs {time_label}")
        plt.grid(True)
        
        # Delay showing the plot until explicitly requested
        if show:
            plt.show()

    def show_all(self):
        """Show all the plots generated so far."""
        plt.show()