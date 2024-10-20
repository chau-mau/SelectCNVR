import click
import numpy as np
import pandas as pd
from itertools import combinations
from scipy.stats import zscore

def load_cnv(cnvr):
    raw_cnv_data = pd.read_csv(cnvr, sep='\t', low_memory=False)
    header_ay = np.array(raw_cnv_data.columns.tolist())
    sample_id = header_ay[3:]
    n_sample = len(sample_id)
    print('Sample number: %s' % n_sample)
    cnv_data_ay = raw_cnv_data.iloc[:, 3:].astype(np.float64).values
    raw_cnv_data = np.vstack((header_ay, raw_cnv_data.astype(np.unicode_).values))
    return sample_id, cnv_data_ay, raw_cnv_data

def cal_vst(cnv_group1, cnv_group2):
    var1 = np.var(cnv_group1, ddof=1)
    var2 = np.var(cnv_group2, ddof=1)
    VT = np.var(np.concatenate((cnv_group1, cnv_group2), axis=0))
    VS = (len(cnv_group1) * var1 + len(cnv_group2) * var2) / (len(cnv_group1) + len(cnv_group2))
    VST = (VT - VS) / VT
    return VST

def load_group(group_file):
    group_dict = {}
    group_set = set()
    with open(group_file) as f:
        for line in f:
            line = line.strip().split('\t')
            group_dict[line[0]] = line[1]
            group_set.add(line[1])
    return group_dict, group_set

def loop_cal(cnv_data_ay, group_set, group_dict, sample_id):
    group_ay = np.array([group_dict.get(x) for x in sample_id])
    cnv_dict = {}
    VST_dict = {}
    ZVST_dict = {}
    combine_list = []
    
    for group in group_set:
        cnv_dict[group] = cnv_data_ay.T[group_ay == group].T
    
    for group1, group2 in combinations(group_set, 2):
        head = '%s-%s' % (group1, group2)
        vst_list = []
        for n_cnv, cnv in enumerate(cnv_data_ay):
            cnv_group1 = cnv[group_ay == group1]
            cnv_group2 = cnv[group_ay == group2]
            vst = cal_vst(cnv_group1, cnv_group2)
            vst_list.append(vst)
        vst_ay = np.array(vst_list)
        zvst_ay = zscore(vst_ay)
        VST_dict[head] = vst_ay
        ZVST_dict[head] = zvst_ay
        combine_list.append(head)
    
    return VST_dict, ZVST_dict, combine_list

def output(raw_cnv_data, VST_dict, ZVST_dict, combine_list, outfile):
    with open(outfile, 'w') as f:
        for n_line, line in enumerate(raw_cnv_data, -1):
            line = [x.strip() for x in line]
            f.write('\t'.join(line[:3]) + '\t')
            if n_line != -1:
                vst_list = [str(VST_dict[x][n_line]) for x in combine_list]
                f.write('\t'.join(vst_list) + '\n')
            else:
                f.write('\t'.join(combine_list) + '\n')

@click.command()
@click.option('--cnvr', help='CNVR file or genotype file')
@click.option('--group', help='Group file (format: Individual ID \\t Group Name)')
@click.option('--out', help='Output result file')
def main(cnvr, group, out):
    sample_id, cnv_data_ay, raw_cnv_data = load_cnv(cnvr)
    group_dict, group_set = load_group(group)
    VST_dict, ZVST_dict, combine_list = loop_cal(cnv_data_ay, group_set, group_dict, sample_id)
    output(raw_cnv_data, VST_dict, ZVST_dict, combine_list, out)

if __name__ == '__main__':
    main()
