#!/usr/bin/env nextflow

/*
 * merge excel files
 */

process merge_excel {

    publishDir 'results', mode: 'copy'

    input:
        path excel_files
        path 'merge_excel.py'

    output:
        path "merged_results.xlsx"

    script:
    """
    python3 merge_excel.py
    """

}