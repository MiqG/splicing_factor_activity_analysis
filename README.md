# Splicing Factor Activity Analysis

Estimate splicing factor activities from changes in exon inclusion or gene expression.

## Requirements

Install conda/mamba environment:

```shell
mamba install -f environment.yaml
```

## Usage
### From exon inclusion signatures (DeltaPSI)

1. Check inputs:
    - exon inclusion signatures as delta PSIs ([`files/examples/signatures/Danielsson2013-EX.tsv.gz`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/examples/signatures/Danielsson2013-EX.tsv.gz)):
        ```shell
        $ zcat Danielsson2013-EX.tsv.gz | head -20
        EVENT	SRR837859	SRR837861	SRR837858	SRR837860	SRR837864	SRR837862	SRR837865	SRR837863
        HsaEX0067681	0.0	0.0	0.0	6.54	0.0	0.0	5.26	8.86
        HsaEX6078702	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
        HsaEX0010105								
        HsaEX0010107								
        HsaEX0010102		0.0	0.0		0.0	0.0	0.0	0.0
        HsaEX6034797								
        HsaEX6034795								
        HsaEX0010108								
        HsaEX6035727	0.0	0.0	0.0	0.0				
        HsaEX0026577	-0.24	-0.24	0.24	-0.24	-0.24	0.09000000000000002	-0.24	-0.24
        HsaEX1015356		0.0	0.0					
        HsaEX1015357								
        HsaEX0027220								
        HsaEX0035417	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
        HsaEX0057075								
        HsaEX0057076								
        HsaEX0004223	0.0	0.0	0.0	0.0			0.0	
        HsaEX6008957	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
        HsaEX0004224	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
        ```

    - splicing factor-exon network(s) directory ([`files/sf_networks/exon_based/exon_inclusion`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/sf_networks/exon_based/exon_inclusion)):
        ```shell
        .
        ├── ENASFS-metaexperiment0-delta_psi.tsv.gz
        ├── ENASFS-metaexperiment1-delta_psi.tsv.gz
        ├── ENASFS-metaexperiment2-delta_psi.tsv.gz
        ├── ENASFS-metaexperiment3-delta_psi.tsv.gz
        ├── ENCOREKD-HepG2-delta_psi.tsv.gz
        ├── ENCOREKD-K562-delta_psi.tsv.gz
        ├── ENCOREKO-HepG2-delta_psi.tsv.gz
        ├── ENCOREKO-K562-delta_psi.tsv.gz
        └── Rogalska2024-HELA_CERVIX-delta_psi.tsv.gz
        ```

2. Estimate splicing factor activity:
    ```shell
    set -eo pipefail

    conda activate sfaa
    
    SIGNATURE_FILE="files/examples/signatures/Danielsson2013-EX.tsv.gz"
    REGULONS_DIR="files/sf_networks/exon_based/exon_inclusion"
    OUTPUT_FILE="sf_activity-exon_based.tsv.gz"
    
    Rscript scripts/compute_protein_activity.R \
                --signature_file=$SIGNATURE_FILE \
                --regulons_path=$REGULONS_DIR \
                --output_file=$OUTPUT_FILE
    ```
    
3. Check output:
    - exon inclusion-based splicing factor activity estimation ([`files/examples/outputs/sf_activity-exon_based.tsv.gz`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/examples/outputs/sf_activity-exon_based.tsv.gz)):
        ```shell
        ```

### From gene expression signatures (log2FC)

1. Check inputs:
    - gene expression signatures as log2 fold changes ([`files/examples/signatures/Hodis2022-invitro_eng_melanoc-genexpr_cpm.tsv.gz`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/examples/signatures/Hodis2022-invitro_eng_melanoc-genexpr_cpm.tsv.gz)):
        ```shell
        ENSEMBL	CB___2.CB___Engineered_melanocytes___False	C___1.C___Engineered_melanocytes___False	CBT3___4a.CBT3___Engineered_melanocytes___False	CBTP___4c.CBTP___Engineered_melanocytes___False	WT___0.WT_p15___Engineered_melanocytes___True	CBTA___4b.CBTA___Engineered_melanocytes___False	CBTPA___5b.CBTPA___Engineered_melanocytes___False	CBT_228___3a.CBT_228___Engineered_melanocytes___False	CBTP3___5a.CBTP3___Engineered_melanocytes___False
        ENSG00000225880	0.015033017024177434	0.0007221241768273594	-0.001326681835879362	-0.011634674664527105	0.0	0.02204721324651151	-0.009283984704949698	-0.004208418758251628	-0.006781458508999312
        ENSG00000230368	0.008834186692369024	0.03297009708619892	-0.012515558524019178	-0.00737275572783333	0.0	0.01974215511470876	0.024510758392757542	0.0038867919871616932	0.010059099956599538
        ENSG00000187634	0.002798945597041462	0.009254613976477623	-0.011591989392351596	-0.011591989392351596	0.0	-0.008009674115254321	-0.010200885926577018	-0.0027104746062760737	-0.010055261084698683
        ENSG00000188976	0.13776594329722058	0.10714158515781913	0.3236987218113786	0.3654918145467325	0.0	0.592650283978732	0.3720098192436482	0.2005114278968616	0.496602891321664
        ENSG00000187961	0.016761721059070943	0.006010821820807047	0.01560345263233142	-0.003465888187115393	0.0	0.016571518810484444	7.62626185643045e-05	0.01336850419161923	0.0241095115315716
        ENSG00000187583	0.012462950927146502	0.004226873714600576	0.005237597529406403	0.0	0.0	0.00950953057642106	0.0037464302831494664	0.007652106537371826	0.002438727151771623
        ENSG00000187642	0.0019214469863386772	0.0	0.0	0.0017357811780067682	0.0	0.01595962014623427	0.003873845438902243	0.0	0.0
        ENSG00000188290	0.1726936190466145	0.11906026740919991	0.10628602155165805	-0.013281331422035789	0.0	0.5054176071205095	-0.013034258899833541	0.11958176445836867	-0.013954462577949266
        ENSG00000187608	3.9355293936638462	1.2539709571985755	0.3934003049562114	0.08977045613573087	0.0	0.056795026007090854	0.11685303471019193	0.4375378837545197	-0.0526845479583668
        ENSG00000188157	0.2768919059824029	0.1334101688954991	0.001273020433597838	-0.02183782742970694	0.0	-0.003971120286696453	-0.006565343449415555	0.010188503539492813	-0.02097559643474098
        ENSG00000131591	0.011826913712432066	0.022964951608294704	0.030307165261759736	0.05605010960949637	0.0	0.060085945062967785	0.0002753475635975944	0.06027819206549438	0.02641095620357216
        ENSG00000186827	0.0	0.0	0.0	0.00522914112192143	0.0	0.0	0.008402024270541358	0.0	0.0021415190929118546
        ENSG00000078808	0.22886353756891675	0.03980294295982212	0.10106149825727395	0.14342223832806789	0.0	0.16374807477575892	0.17323302402954566	0.15944619743193633	0.14818605990692446
        ENSG00000176022	0.2343445620455089	0.032236766830964936	0.34769932607719967	0.33518904318106024	0.0	0.2672363404592806	0.23755347219194178	0.24197072064473457	0.2604265658287187
        ENSG00000184163	0.012473770464169599	0.008931956054040008	0.007478495275873173	0.00950289322168304	0.0	0.006084775557361288	0.0007901391070591966	0.019941281121856662	0.006966674915650881
        ENSG00000160087	-0.0003019777083455022	0.02237642953069996	0.24904421070382243	0.164309243907917	0.0	0.5279741975062573	0.20692856018743	0.15406223362959126	0.3004978545622379
        ENSG00000230415	0.00197443983313287	0.0	0.0	0.0	0.0	0.0	0.0	0.002227499397856332	0.0019886204382837964
        ENSG00000162572	0.005252275446532034	0.0028829882561829012	0.001765970373836067	0.008701866680255797	0.0	0.0024442161291655788	0.009206776740800317	-0.00030577908938497376	-0.0024344249592753125
        ENSG00000131584	0.02622141315067883	-0.027181458058897212	0.044197056319507655	-0.001393788362747117	0.0	0.010157462257172678	-0.03142404756322281	0.003767481978802223	-0.028600569662224573
        ```

    - splicing factor-gene network(s) directory ([`files/sf_networks/gene_based/bulkgenexpr`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/sf_networks/gene_based/bulkgenexpr)):
        ```shell
        .
        ├── ENASFS-metaexperiment0-log2fc_genexpr.tsv.gz
        ├── ENASFS-metaexperiment1-log2fc_genexpr.tsv.gz
        ├── ENASFS-metaexperiment2-log2fc_genexpr.tsv.gz
        ├── ENASFS-metaexperiment3-log2fc_genexpr.tsv.gz
        ├── ENCOREKD-benchmark-log2fc_genexpr.tsv.gz
        ├── ENCOREKO-benchmark-log2fc_genexpr.tsv.gz
        └── Rogalska2024-HELA_CERVIX-log2fc_genexpr.tsv.gz
        ```

    - adjustment model for gene-baed estimation of splicing factor activity ([`files/adj_models/gene_based/bulkgenexpr`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/adj_models/gene_based/bulkgenexpr)): 
        ```shell
        .
        ├── input_regulators.tsv.gz
        ├── output_regulators.tsv.gz
        ├── weights-0.pth
        ├── weights-1.pth
        ├── weights-2.pth
        ├── weights-3.pth
        └── weights-4.pth
        ```

2. Estimate splicing factor activity:
    ```shell
    set -eo pipefail
    
    conda activate sfaa

    SIGNATURE_FILE="files/examples/signatures/Hodis2022-invitro_eng_melanoc-genexpr_cpm.tsv.gz"
    REGULONS_DIR="files/sf_networks/gene_based/bulkgenexpr"
    ADJ_MODELS_DIR="files/adj_models/gene_based/bulkgenexpr"
    OUTPUT_FILE="sf_activity-gene_based.tsv.gz"
    TMP_DIR="."
    
    # estimate gene-based activity
    Rscript scripts/compute_protein_activity.R \
                --signature_file=$SIGNATURE_FILE \
                --regulons_path=$REGULONS_DIR \
                --output_file=$TMP_DIR/unadjusted_gene_based_activity.tsv.gz
                
    # adjust gene-based activity
    python scripts/adjust_genexpr_sf_activity.py \
                --activity_file=$TMP_DIR/unadjusted_gene_based_activity.tsv.gz \
                --models_dir=$ADJ_MODELS_DIR \
                --output_file=$OUTPUT_FILE
                
    # remove temporary files
    rm $TMP_DIR/unadjusted_gene_based_activity.tsv.gz
    ```
    
3. Check output:
    - exon inclusion-based splicing factor activity estimation ([`files/examples/outputs/sf_activity-gene_based.tsv.gz`](https://github.com/MiqG/splicing_factor_activity_analysis/tree/main/files/examples/outputs/sf_activity-gene_based.tsv.gz)):
        ```shell
        ```

## Issues
Please, report any issues here: https://github.com/MiqG/splicing_factor_activity_analysis/issues

## Citation
(TODO)
