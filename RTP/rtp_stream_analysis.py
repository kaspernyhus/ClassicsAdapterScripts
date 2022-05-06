import pandas as pd
import matplotlib.pyplot as plt

# Import CSV data, skip first row, include columns 0125
df = pd.read_csv('RTP_data/RTP_Packet_Data.csv', skiprows=1, header=None, usecols=[0, 1, 2, 5])
df.columns = ['Packet', 'Sequence', 'Delta', 'Bandwidth']
print(df)


# Statistics
bandwidth_avg = df['Bandwidth'].mean()
print("------------------------------------------------")
print("  Statistics")
print("------------------------------------------------")
print("Max delta [ms]:", df['Delta'].max())
print("Average delta [ms]:", df['Delta'].mean())
print("Average bandwidth [kbit/s]:", bandwidth_avg)




ax = df.plot(y='Delta')
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
# ax.set_ylim([0, ax.axes.get_ylim()[1]])
plt.ylabel("Packets delta delay [ms]")
plt.show()

