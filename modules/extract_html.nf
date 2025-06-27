#!/usr/bin/env nextflow

/*
 * extract information from HTML files
 */

process extract_html {

    publishDir 'results/extracted_html', mode: 'copy'

    input:
        tuple path(html_file), val(assay_type), val(source)
        path 'extract_html.py'

    output:
        path "${html_file.simpleName}.xlsx"

    script:
    """
    python3 extract_html.py $html_file $assay_type $source
    """
}