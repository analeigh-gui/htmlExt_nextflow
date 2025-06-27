#!/usr/bin/env nextflow

include { extract_html } from './modules/extract_html.nf'
include { merge_excel } from './modules/merge_excel.nf'

/*
 * Pipeline parameters
 */
params.input = 'input.csv'

// Workflow block
workflow {
    ch_html_files = Channel.fromPath(params.input)
                            .splitCsv(header: false, sep: ';')
                            .map { row -> tuple(file(row[0]), row[1], row[2])}

    // Channel for the scripts
    ch_script = Channel.value(file('extract_html.py'))
    ch_merge_script = Channel.value(file('merge_excel.py'))

    // Extract information from HTML files
    excel_outputs = extract_html(ch_html_files, ch_script)

    // Collect all Excel files and merge them
    all_excel = excel_outputs.collect()

    // Merge all Excel files into one
    merge_excel(all_excel, ch_merge_script)
}