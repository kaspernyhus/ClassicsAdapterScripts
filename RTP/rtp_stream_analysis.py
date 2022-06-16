import pandas as pd
import matplotlib.pyplot as plt


#
# Wireshark -> Telephony -> RTP -> RTP Streams -> Analyse -> Save -> Forward Stream CSV
#

def get_quantile(df, lower, upper):
    if lower == 0:
        return df[(df['Delta'] < upper)]['Delta'].sum() / df['Delta'].sum() * 100
    elif upper == 'max':
        return df[(df['Delta'] > lower)]['Delta'].sum() / df['Delta'].sum() * 100
    else:
        return df[(df['Delta'] > lower) & (df['Delta'] < upper)]['Delta'].sum() / df['Delta'].sum() * 100


def rtp_analyse(filename, bandwidth=False):
    # Import CSV PCM_data, skip first row, include columns 0125
    df = pd.read_csv(filename, skiprows=1, header=None, usecols=[0, 1, 2, 5])
    df.columns = ['Packet', 'Sequence', 'Delta', 'Bandwidth']
    # print(df)
    filename = filename.split('/')[1]

    # Statistics
    bandwidth_avg = df['Bandwidth'].mean()
    q1 = get_quantile(df, 0, 3)
    q2 = get_quantile(df, 3, 10)
    q3 = get_quantile(df, 10, 50)
    q4 = get_quantile(df, 50, 100)
    q5 = get_quantile(df, 100, 200)
    q6 = get_quantile(df, 200, 300)
    q7 = get_quantile(df, 300, 'max')

    print("-----------------------------------------------------")
    print("  Statistics", filename)
    print("-----------------------------------------------------")
    print("Max delta [ms]:", round(df['Delta'].max(), 2))
    print("Average delta [ms]:", round(df['Delta'].mean(), 2))
    print("Average bandwidth [kbit/s]:", round(bandwidth_avg, 2))
    print("\n---- Delay distribution -----")
    print("Below 3ms    :", round(q1, 1), "%")
    print("3ms - 10ms   :", round(q2, 1), "%")
    print("10ms - 50ms  :", round(q3, 1), "%")
    print("50ms - 100ms :", round(q4, 1), "%")
    print("100ms - 200ms:", round(q5, 1), "%")
    print("200ms - 300ms:", round(q6, 1), "%")
    print("above 300ms  :", round(q7, 1), "%")

    ax = df.plot(y='Delta')
    # ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    # ax.set_ylim([0, ax.axes.get_ylim()[1]])
    plt.ylabel("Packets delta delay [ms]")
    plt.title("RTP packet delay. File: "+filename)
    plt.ylim(0, 600)

    if(bandwidth):
        df.plot(y='Bandwidth')
        plt.ylabel("Bandwidth [kbit/s]")

    plt.figure()
    barax = plt.bar(['<3ms', '3-10ms', '10-50ms', '50-100ms', '100-200ms', '200-300ms', '>300ms'],
                    [round(q1, 1), round(q2, 1), round(q3, 1), round(q4, 1), round(q5, 1), round(q6, 1), round(q7, 1)])
    plt.bar_label(barax)
    plt.xticks(rotation=45)
    plt.ylabel("%")
    plt.title("RTP packet delay distribution. File: "+filename)
    plt.ylim(0, 100)
    plt.tight_layout()
    # plt.show()


filename1 = 'RTP_data/RTP Packet Data test4.csv'
filename2 = 'RTP_data/RTP_Packet_Data_home_static32.csv'
rtp_analyse(filename1)
rtp_analyse(filename2)
plt.show()

