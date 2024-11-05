import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import ticker

class Plotter:
    def __init__(self, filename="log.csv"):
        self.filename = filename
        self.data = None
    
    def load_data(self):
        """Loads data from a CSV file."""
        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename)
            print(f"[Plotter] Data loaded from \"{self.filename}\"")
        else:
            raise FileNotFoundError(f"{self.filename} does not exist in the directory.")
    
    def plot_columns(self, columns=None, show=False, override_title=None, override_x_label=None, override_y_label=None, connect_data=True, x_major_unit=None, y_major_unit=None, y_axis_limits=None):
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
            if connect_data:
                plt.plot(time, self.data[column], label=clean_column_name)  # Connect data with lines
            else:
                plt.scatter(time, self.data[column], label=clean_column_name)  # Plot data points without connecting
        
        # Override labels and title if provided
        plt.xlabel(override_x_label if override_x_label else time_label)
        plt.ylabel(override_y_label if override_y_label else f"Values of {concatenated_columns}")
        plot_title = override_title if override_title else f"Plot of {concatenated_columns} vs {time_label}"
        plt.title(plot_title)
        plt.legend()
        plt.grid(True)

        # Set x-axis major units if specified
        if x_major_unit is not None:
            plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(x_major_unit))
        
        # Set y-axis major units if specified
        if y_major_unit is not None:
            plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(y_major_unit))

        # Set y-axis limits if specified
        if y_axis_limits is not None:
            plt.ylim(y_axis_limits)
        else:
            # Automatically adjust y-axis to cover all data points
            all_y_values = pd.concat([self.data[col] for col in columns])
            plt.ylim(all_y_values.min(), all_y_values.max())
        
        # Automatically adjust plot to fit labels and title within the figure
        plt.tight_layout()

        # Create "Plots" directory if it doesn't exist
        if not os.path.exists("Plots"):
            os.makedirs("Plots")

        # Save the plot in the "Plots" directory with a filename matching the title
        sanitized_title = plot_title.replace(" ", "_").replace(",", "").replace("/", "_")
        save_path = os.path.join("Plots", f"{sanitized_title}.png")
        plt.savefig(save_path, format='png', transparent=True)
        print(f"Figure saved at {save_path} with no background.")

        # Delay showing the plot until explicitly requested
        if show:
            plt.show()

    def show_all(self):
        """Show all the plots generated so far."""
        plt.show()
