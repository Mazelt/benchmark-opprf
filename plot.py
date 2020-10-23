import matplotlib.pyplot as plt
import os.path
import glob
import json


def load_batch(pattern):
    os.path.exists('./batchlogs/experiments')
    files = glob.glob(f"./batchlogs/experiments/Batch-{pattern}*.json")
    files = sorted(files)
    for i,e in enumerate(files):
        print(f"{i}:\t {e}")
    all_right = input('Take all? Press any key to continue')
    batches = []
    for f in files:
        with open(f, 'r') as fp:
            b = json.load(fp)
            for batch in batches:
                if batch['parameters'] == b['parameters']:
                    batch[b['repeat']] = {
                        's_output': b['s_output'], 'c_output': b['c_output']}
                    b = 0
                    break
            if b:
                batches.append({'parameters':b['parameters'], b['repeat']: {'s_output': b['s_output'], 'c_output': b['c_output']}})
    return batches
    # list batch files that match a pattern
    # later choose from them. now take them all.
    # load batch
    # return data object

def plot_hashing(data):
    # simple plot right now.
    print('Hashing')

    for b in data:
        print(b['parameters']['client_neles'])
        s_hashing_t = []
        c_hashing_t = []
        for i in range(len(b)-1):
            s_hashing_t.append(b[i]['s_output']['hashing_t'])
            c_hashing_t.append(b[i]['c_output']['hashing_t'])
        print(f"Server hashing time: {sum(s_hashing_t)/(len(b)-1)}")
        print(f"Client hashing time: {sum(c_hashing_t)/(len(b)-1)}")

if __name__ == '__main__':
    data = load_batch('ScalingElementsDA_2')
    plot_hashing(data)
# def plot_calibration_plots(y_true, probs={}):
#     # calibration plots (https://scikit-learn.org/stable/auto_examples/calibration/plot_compare_calibration.html)
#     plt.figure(figsize=(10,10))
#     ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2)
#     ax2 = plt.subplot2grid((3,1), (2,0))
#     ax1.plot([0,1],[0,1], 'k', label='Perfectly calibrated')
#     for k, v in probs.items():
#         fraction_of_positives, mean_predicted_value = \
#             calibration_curve(y_true,v, n_bins=10)
#         ax1.plot(mean_predicted_value, fraction_of_positives, 's-',
#                  label=f'{k}')
#         ax2.hist(v, range=(0,1), bins=10, label=k, histtype='step', lw=2)
#     ax1.set_ylabel("Fraction of positives")
#     ax1.set_ylim([-0.05, 1.05])
#     ax1.legend(loc="lower right")
#     ax1.set_title('Calibration plots  (reliability curve)')

#     ax2.set_xlabel("Mean predicted value")
#     ax2.set_ylabel("Count")
#     ax2.legend(loc="upper center", ncol=2)

#     plt.tight_layout()
#     plt.show()


# def plot_roc_curve(y_true, probs={}):
#     fpr1, tpr1, _ = metrics.roc_curve(y_true, probs['mpc'])
#     fpr2, tpr2, _ = metrics.roc_curve(y_true, probs['sklearn'])

#     plt.plot(fpr1, tpr1, marker='.', label='mpc')
#     plt.plot(fpr2, tpr2,  marker='.', label='sklearn')
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')

#     plt.legend()
#     plt.show()


# def plot_precision_recall(y_true, probs={}):
#     mpc_prec, mpc_recall, _ = metrics.precision_recall_curve(
#         y_true, probs['mpc'])
#     sklearn_prec, sklearn_recall, _ = metrics.precision_recall_curve(
#         y_true, probs['sklearn'])
#     plt.plot(mpc_recall, mpc_prec, marker='.', label='mpc')
#     plt.plot(sklearn_recall, sklearn_prec, marker='.', label='sklearn')
#     plt.xlabel('Recall')
#     plt.ylabel('Precision')
#     plt.legend()
#     plt.show()
