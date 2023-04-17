def detonate_file(provides, all_app_runs, context):
    for summary, action_results in all_app_runs:
        for result in action_results:
            context['data'] = result.get_data()[0]
            context['param'] = result.get_param()

    return 'views/reversinglabs_detonate_file.html'


def detonate_and_get_report(provides, all_app_runs, context):
    return get_report(provides, all_app_runs, context)
    # for summary, action_results in all_app_runs:
    #     for result in action_results:
    #         context['data'] = result.get_data()[0].get('tc_report')
    #         context['param'] = result.get_param()

    # return 'views/reversinglabs_report.html'


def get_report(provides, all_app_runs, context):
    for summary, action_results in all_app_runs:
        for result in action_results:
            context['data'] = result.get_data()[0].get('tc_report')[0]
            context['param'] = result.get_param()
            context["classification"] = get_status_from_ticore_classification(
                context['data'].get("classification").get("classification")
            ).upper()
            context["classification_color"] = color_code_classification(context["classification"])

    return 'views/reversinglabs_report.html'


def color_code_classification(classification):
    color = ""
    classification = classification.upper()
    if classification == 'MALICIOUS':
        color = "red"
    elif classification == 'SUSPICIOUS':
        color = "orange"
    elif classification == 'KNOWN':
        color = "green"
    elif classification == 'GOODWARE':
        color = "green"

    return color


def get_status_from_ticore_classification(classification_int):
    status_mapping = {
        3: "malicious",
        2: "suspicious",
        1: "known"
    }

    return status_mapping.get(classification_int, 'unknown')
