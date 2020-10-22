"""
exporting to latex guide: https://timodenk.com/blog/exporting-matplotlib-plots-to-latex/

graphing guides:
- https://matplotlib.org/3.1.1/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py



"""
import math
import matplotlib.pyplot as plt
import csvReader
import pandas as pd
import numpy as np

import render_sankey_diagram
from data_parser import dtypes, format_as_percentage, dates, remove_byte_string
from numpy.polynomial.polynomial import polyfit


def spread_of_data_sub_to_stars(data):
    plot = plt
    plot.xlabel('stars')
    plot.ylabel('subscribers')

    x = []
    y = []
    for line in data:
        x.append(int(line.get("stargazers_count")))
        y.append(int(line.get("subscribers_count")))
    plot.scatter(x, y, s=1, alpha=0.75, label="project")

    plot.legend()
    return plot


def lines_against_scripts(data):
    data["scripts"] = data["bash"] + data["powershell"]
    plot = plt
    plot.xlabel('no. lines in file')
    plot.ylabel('no. scripts used in file')
    x = data["code"]
    y = data["scripts"]
    b, m = polyfit(x, y, 1)
    plot.plot(x, b + m * x, '-', color="red",
              alpha=0.25, scalex=False, scaley=False)
    # plot.plot(np.array(range(x.max())), np.array(range(x.max())), '-', color="green", alpha=0.25)

    plot.scatter(x, y, s=0.5, alpha=0.5)
    plot.xlim(0, 250)
    plot.ylim(0, 50)

    return plot


def stars_against_lines(data):
    data["scripts"] = data["bash"] + data["powershell"]
    plot = plt
    plot.xlabel('stars')
    plot.ylabel('no. scripts used in file')
    # data = data.sort_values(by=["stars"])
    x = data["stars"]
    y = data["scripts"]
    b, m = polyfit(x, y, 1)
    plot.plot(x, b + m * x, '-', color="red",
              alpha=0.25, scalex=False, scaley=False)
    # plot.plot(np.array(range(x.max())), np.array(range(x.max())), '-', color="green", alpha=0.25)
    plot.scatter(x, y, s=0.5, alpha=0.5)
    plot.ylim(0, 50)
    plot.xlim(0, 20000)

    return plot


def spread_of_data_v2(data, sorted_data):
    plot = spread_of_data_sub_to_stars(data)

    x = []
    y = []
    for line in sorted_data:
        x.append(int(line.get("stars")))
        y.append(int(line.get("sub")))
    plot.scatter(x, y, s=1, alpha=0.3)

    return plot


def spread_data_issues_vs_stars(data):
    plot = plt
    plot.xlabel('stars')
    plot.ylabel('issues')

    x = []
    y = []
    for line in data:
        x.append(int(line.get("stargazers_count")))
        y.append(int(line.get("open_issues")))

    plot.scatter(x, y, s=1, alpha=0.75)

    plot.legend()
    return plot


def spread_of_data_line_star(data, sorted_data):
    stars = {}
    for line in data:
        stars[int(line.get("id"))] = (int(line.get("stargazers_count")), 0)

    for line in sorted_data:
        stars[int(line.get("id"))] = (int(line.get("stars")), 1)
    return create_percentage_bar_graphs(list(stars.values()), "percentage of stars that use CI", "stars")


def ci_usage_against_commits(data, sorted_data):
    stars = {}
    for line in data:
        if line.get("commits") == "":
            stars[int(line.get("id"))] = (0, 0)
        else:
            stars[int(line.get("id"))] = (int(line.get("commits")), 0)

    for line in sorted_data:
        if line.get("commits") == "":
            stars[int(line.get("id"))] = (0, 1)
        else:
            stars[int(line.get("id"))] = (int(line.get("commits")), 1)
    return create_percentage_bar_graphs(list(stars.values()), "percentage of stars that use CI", "stars")


def spread_of_data_line_sub(data, sorted_data):
    stars = {}
    for line in data:
        stars[int(line.get("id"))] = (int(line.get("subscribers_count")), 0)

    for line in sorted_data:
        stars[int(line.get("id"))] = (int(line.get("sub")), 1)
    return create_percentage_bar_graphs(list(stars.values()), "percentage of subscriptions that use CI", "subscribers")


def spread_of_data_line_star_other_paper():
    data = csvReader.readfile("breadth_corpus.csv")
    results = []
    for line in data:
        if line.get("CI") and int(line.get("CI")) > 0:
            results.append((int(line.get("stars")), 1))
        else:
            results.append((int(line.get("stars")), 0))

    return create_percentage_bar_graphs(results, "percentage of stars that use CI", "stars")


def create_percentage_bar_graphs(stars, name, xname, grouping_amount=540):
    stars.sort(key=lambda x: x[0])
    groups = []
    j = 0
    i = 1
    while j < len(stars):
        group = []
        while j < grouping_amount * i and j < len(stars):
            group.append(stars[j][1])
            # group.append((stars[keys[j]], keys[j]))
            j += 1
        groups.append((stars[j - 1][0], group))
        i += 1

    heights = []
    bottom = []
    for group in groups:
        bottom.append(group[0])
        if len(group[1]) != 0:
            heights.append((sum(group[1]) / len(group[1])) * 100)
        else:
            heights.append(0)

    fig, ax = plt.subplots()

    # We need to draw the canvas, otherwise the labels won't be positioned and
    # won't have values yet.

    # so what happens here is we set the positions for all the bars
    # then with those positions we set the label
    # the key here that ax.bar primarily takes positions and then works out labels after that
    # so that means you can't try do clever stuff as it will work out the positions first which will muck up
    # all the things

    ax.bar(np.arange(len(bottom)), heights)
    plt.rc(({'font.size': 9}))
    plt.xticks(rotation=90)

    plt.title(name)
    plt.ylim(0, 100)
    plt.xlabel(xname)
    plt.ylabel("percentage")
    labels = []
    for i in range(len(bottom)):
        if i == len(bottom) - 1:
            labels.append(str(bottom[i]))
        else:
            if i % 5 == 0:
                labels.append(str(bottom[i]))
            else:
                labels.append("")

    # this line is needed here
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, zorder=100)

    # ax.set_xticklabels(labels)
    return fig


def save_as_pdf(plot, name, encoding="pdf"):
    print(f'writing: {name}.{encoding}')
    plot.savefig(f'{name}.{encoding}', bbox_inches='tight')
    # delete the graph
    plot.clf()


def spread_over_time_stars(data):
    plot = plt
    plot.ylabel('stars')
    plot.xlabel('number of projects')
    x = []
    for line in data:
        x.append(int(line.get("stargazers_count")))

    x.sort()
    plot.scatter(list(range(len(x))), x, s=0.5)

    return plot


def boxplot_stars(plot, data):
    """
    kind of works but doesn't create anything that can be easily displayed as all the data is
    grouped up as predicted at one end....

    therefore the line graph still is the best way to show the spread still
    """
    plot.ylabel('stars')
    x = []
    for line in data:
        x.append(int(line.get("stargazers_count")))

    plot.boxplot(x, vert=False, showfliers=False, autorange=True)

    return plot


def load_dataframe(name):
    return pd.read_csv(name, dtype=dtypes, parse_dates=dates)


def _value_counts_bar_graph(plot, data):
    # data.pop("travis")
    # data.pop("github")
    plot.bar(list(data.keys()), [data[k] for k in data.keys()])
    plot.xticks(rotation=45)
    return plot


def _value_counts_bar_graph_log(plot, data):
    print(data.head(5))
    data = data.to_frame()
    print(data.columns)
    print(data.index)
    print(data.keys())
    plot.bar(list(data.keys()), [data[k] for k in data.keys()], width=0.5)
    plot.xticks(rotation=45)
    plot.rc(({'font.size': 5}))
    return plot


def config_bargraph(plot, dataset):
    # returns the config count for all config types
    # note: this doesn't matter if we have multiple configurations in the repo
    return _value_counts_bar_graph_log(plot, dataset.groupby(["id", "lang"])["lang"].value_counts())


def scripts_latex(name, sorted_data):
    frames = []

    df = sorted_data.groupby("config")[
        ["bash", "powershell"]].sum()
    df = df.join(sorted_data.groupby(
        "config").size().rename("number of config"))
    df = df.join((format_as_percentage(
        df["bash"] / df["number of config"] * 100)).rename("percentage bash"))
    df = df.join((format_as_percentage(
        df["powershell"] / df["number of config"] * 100)).rename("percentage powershell"))
    # frames.append({"no. config": })
    #
    # frames.append({"perc bash": frames[0]["bash"] / frames[1]["no. config"] * 100})
    # frames.append({"perc power": frames[0]["powershell"] / frames[1]["no. config"] * 100})

    with open(name, 'w') as tf:
        s = df.to_latex(caption="sum of scripts used", label="table:scripts used",
                        bold_rows=True).replace("\\midrule", "").replace("\\toprule",
                                                                         "\\hline").replace(
            "\\bottomrule", "").replace("\\begin{table}", "").replace("\\end{table}", "").replace("\centering",
                                                                                                  "").replace("\\\\",
                                                                                                              "\\\\ \\hline").replace(
            "lrrrll", "|l|l|l|l|l|l|")
        s = "\n".join([v for v in s.split("\n") if not v.startswith("\\textbf{config")]).replace(
            "yaml\_encoding\_error", "config")
        tf.write(s)


def yaml_config_errors_to_latex(name, dataset):
    df = dataset.groupby(['config', 'yaml_encoding_error']
                         ).size().unstack(fill_value=0)
    thing = dataset[dataset["yaml"]]["config"].value_counts()
    defaults = dict([(k, 0) for k in thing.index if k not in df.index])
    df2 = pd.DataFrame({"composer error": defaults, "constructor error": defaults, "parse error": defaults,
                        "scanner error": defaults})
    df = pd.concat([df, df2])
    df["no. config"] = thing
    with open(name, 'w') as tf:
        s = "\\begin {table}[!htbp]" + df.to_latex(caption="yaml configuration errors", label="table_yaml_errors",
                                                   bold_rows=True).replace("\\midrule", "").replace("\\toprule",
                                                                                                    "\\hline").replace(
            "\\bottomrule", "").replace("\\begin{table}", "").replace("\centering", "").replace("\\\\",
                                                                                                "\\\\ \\hline").replace(
            "lrrrrr", "|l|l|l|l|l|l|")
        s = "\n".join([v for v in s.split("\n") if not v.startswith("\\textbf{config")]) \
            .replace("yaml\_encoding\_error", "config")
        tf.write(s)


def topn(df, n, xaxis):
    names = []
    values = []
    for key, value in df.value_counts().sort_values(ascending=False).head(n).iteritems():
        names.append(key)
        values.append(value)
    plt.bar(names, values)
    plt.rc(({'font.size': 9}))
    plt.xticks(rotation=90)

    plt.xlabel("{} (top {})".format(xaxis, n))
    plt.ylabel("count")
    return plt


def config_topn(df, n):
    names = []
    values = []
    for key, value in df["config"].value_counts().sort_values(ascending=False).head(n).iteritems():
        names.append(key.replace("jenkinsPipeline", "Jenkins"))
        values.append(value)
    total = sum(values)
    plt.rc(({'font.size': 6}))

    plt.bar(names, [(v / total) * 100 for v in values])
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.xlabel("Configuration")
    plt.ylabel("percentage")
    return plt


def langues_topn(df, n):
    return topn(df["lang"], n, "languages")


def popularity_vs_percentage_CI_scatter(df, data):
    plot = plt
    x = []
    y = []
    names = []
    s = []
    for key, value in df["total count"].iteritems():
        s.append((value / df["total count"].max()))

    for key, value in df["percentage CI"].iteritems():
        x.append(float(value.replace("%", "")))
        y.append(data[data["lang"] == key]["stars"].median())
        names.append(key)

    fig, ax = plt.subplots()
    ax.scatter(y, x, [a * 50 for a in s])
    for i, txt in enumerate(names):
        ax.annotate(txt, (y[i], x[i]), fontsize=4 + (s[i] * 5))
    plt.ylim(0, 100)
    plt.xlabel("stars")
    plt.ylabel("percentage")
    return fig


def languages_table_topn(name, n, data, sorted_data):
    data["language"] = data["language"].apply(
        lambda x: x[2:-1] if isinstance(x, str) and x.startswith("b'") else x)
    data["language"] = data["language"].apply(
        lambda x: x[2:-1] if isinstance(x, str) and x.startswith('b"') else x)
    c = data["language"].value_counts
    # data.index.size - data["id"].value_counts().apply(lambda x: x if x == 1 else 0).sum()

    # c2 = sorted_data["lang"].value_counts
    c2 = sorted_data.groupby("lang")["id"].nunique
    frames = {"total count": c(), "using CI": c2(),
              "percentage CI": c2() / c() * 100}
    df = pd.DataFrame(frames)
    # df["percentage CI"] = df["percentage CI"].apply(lambda x: x if x <=100 else -100)
    df["percentage CI"] = format_as_percentage(df["percentage CI"])
    df = df.sort_values("total count", ascending=False)
    df = df.head(n)
    s = df.to_latex(
        caption="Total count of all programming languages used by projects. It has programming languages that only "
                "found once removed.",
        label="table:languages").replace("lrrr", "|l|r|r|r|").replace("\\midrule", "").replace("\\toprule",
                                                                                               "\\hline").replace(
        "\\bottomrule", "")

    with open(name, 'w') as tf:
        tf.write(s)
    print(f"writing data to {name}")
    return df


def _lang(plot, df, sorted_data, key, s):
    categories = {}
    data = sorted_data[key].value_counts()

    for lang_index in range(data.size):
        try:
            temp = df[data.index[lang_index].lower()]
            temp = temp[temp.notnull()]
        except KeyError:
            temp = None
        if temp is not None and temp.size > 0:
            for i in range(temp.size):
                if categories.get(temp[i]) is None:
                    categories[temp[i]] = 0

                if s != 3:
                    categories[temp[i]] += data[lang_index]
                else:
                    categories[temp[i]] += 1

        else:
            if categories.get("unknown") is None:
                categories["unknown"] = 0

            if s != 3:
                categories["unknown"] += data[lang_index]
            else:
                categories["unknown"] += 1

    print(categories.values())
    foo = list(categories.items())
    foo.sort(key=lambda x: x[1], reverse=True)
    foo = foo[:20]
    return plot.bar([v[0] for v in foo if v[0] != " " and v[0] != ""],
                    [v[1] for v in foo if v[0] != " " and v[0] != ""])


def language_type(data, sorted_data):
    fig, ax = plt.subplots()
    df = pd.read_json("langs.json", orient="index").T
    # the T flips the axis so that we get keys for columns and values for the index and we need to do this as the
    # value arrays aren't of equal length
    data["language"] = data["language"].apply(
        lambda x: x[2:-1] if isinstance(x, str) else x)
    rects1 = _lang(ax, df, data, "language", 1)
    rects2 = _lang(ax, df, sorted_data, "lang", 2)

    for i in range(len(rects1)):
        rect = rects1[i]
        height = rect.get_height()
        ax.annotate('{}'.format(format_as_percentage(rects2[i].get_height() / rects1[i].get_height())),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=4)

    plt.xticks(rotation=90)
    return fig


def config_type_split(name, dataset):
    df = dataset["config"].value_counts()
    total = sum([df[k] for k in df.keys()])
    values = ["{:.0%}".format(df[k] / total) for k in df.keys()]
    df = df.to_frame()
    df["percentage"] = values

    s = "\\begin {table}[!htbp]" + df.to_latex(caption="Configuration types spread",
                                               label="table_config_types").replace("\\midrule", "").replace("\\toprule",
                                                                                                            "\\hline").replace(
        "\\bottomrule", "").replace("\\begin{table}", "").replace("\centering", "").replace("\\\\",
                                                                                            "\\\\ \\hline").replace(
        "lrrrr", "|l|l|l|l|l|")

    with open(name, 'w') as tf:
        tf.write(s)


def comment_uage_tbale(data):
    f = {
        "comments": data["comments"].sum() / data["file_lines"].sum(),
        "code": data["code"].sum() / data["file_lines"].sum(),
        "blank lines": data["blank_lines"].sum() / data["file_lines"].sum(),
        "for comments: multiple line": data["multi_line_comment"].sum() / data["comments"].sum(),
        "for comments: single line": data["single_line_comment"].sum() / data["comments"].sum(),
        "for comments: code comment": data["code_with_comments"].sum() / data["comments"].sum(),
    }

    df2 = pd.DataFrame(f, index=[0])

    print(df2.to_latex(caption="yaml configuration errors", label="table_yaml_errors",
                       bold_rows=True))


def line_usage_configuration(data, only_comments=False):
    import numpy as np
    # set width of bar
    barWidth = 0.25
    if only_comments:
        data = data[data["comments"] > 0]
    df = data.groupby("config")[
        ["blank_lines", "comments", "code", "file_lines"]].mean()

    bars = []
    for config in df.columns:
        bars.append(list(df[config]))

    # Set position of bar on X axis
    r1 = np.arange(len(bars[0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    # Make the plot
    plt.bar(r1, bars[0], color='#7f6d5f', width=barWidth,
            edgecolor='white', label='blank lines')
    plt.bar(r2, bars[1], color='#557f2d', width=barWidth,
            edgecolor='white', label='comments')
    plt.bar(r3, bars[2], color='blue', width=barWidth,
            edgecolor='white', label='code')
    plt.bar(r4, bars[3], color='red', width=barWidth,
            edgecolor='white', label='file lines')

    # Add xticks on the middle of the group bars
    plt.ylabel("mean number of lines", fontweight='bold')
    plt.xlabel('configuration', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars[0]))], list(df.index))
    plt.xticks(rotation=45)
    plt.legend()
    return plt


def line_usage_configuration2(data, only_comments=False):
    import numpy as np
    # set width of bar
    barWidth = 0.25
    if only_comments:
        data = data[data["comments"] > 0]
    df = data.groupby("config")[["comments", "code_with_comments",
                                 "single_line_comment", "multi_line_comment"]].mean()

    bars = []
    for config in df.columns:
        bars.append(list(df[config]))

    # Set position of bar on X axis
    r1 = np.arange(len(bars[0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    # Make the plot
    plt.bar(r1, bars[0], color='#7f6d5f', width=barWidth,
            edgecolor='white', label='comments')
    plt.bar(r2, bars[1], color='blue', width=barWidth,
            edgecolor='white', label='code with comments')
    plt.bar(r3, bars[2], color='red', width=barWidth,
            edgecolor='white', label='single line comment')
    plt.bar(r4, bars[3], color='#2d7f5e', width=barWidth,
            edgecolor='white', label='multi line comment')

    # Add xticks on the middle of the group bars
    plt.ylabel("mean number of lines", fontweight='bold')
    plt.xlabel('configuration', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars[0]))], list(df.index))
    plt.xticks(rotation=45)
    plt.legend()
    return plt


def comment_usage(data):
    import numpy as np
    # set width of bar
    barWidth = 0.25

    df = data[data["comments"] > 0].groupby(
        "config")[["version", "http", "header", "important", "todo"]].mean()
    print(df)
    # set height of bar
    # bars1 = [12, 30, 1, 8, 22]
    # bars2 = [28, 6, 16, 5, 10]
    # bars3 = [29, 3, 24, 25, 17]
    #
    bars = []
    for config in df.columns:
        bars.append(list(df[config]))

    # Set position of bar on X axis
    r1 = np.arange(len(bars[0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]

    # Make the plot
    plt.bar(r1, bars[0], color='#7f6d5f', width=barWidth,
            edgecolor='white', label=df.columns[0])
    plt.bar(r2, bars[1], color='#557f2d', width=barWidth,
            edgecolor='white', label=df.columns[1])
    plt.bar(r3, bars[2], color='blue', width=barWidth,
            edgecolor='white', label=df.columns[2])
    plt.bar(r4, bars[3], color='red', width=barWidth,
            edgecolor='white', label=df.columns[3])
    plt.bar(r5, bars[4], color='#2d7f5e', width=barWidth,
            edgecolor='white', label=df.columns[4])

    # Add xticks on the middle of the group bars
    plt.ylabel("average")
    plt.xlabel('configuration', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars[0]))], list(df.index))
    plt.xticks(rotation=45)
    plt.legend()
    return plt


def script_usage(data):
    import numpy as np
    # set width of bar
    barWidth = 0.25

    df = data[(data["powershell"] > 0) | (data["bash"] > 0)].groupby(
        "config")[["bash", "powershell"]].mean()
    df2 = data.groupby("config")[["bash", "powershell"]].mean()
    bars = []
    # bars2 = []
    for config in df2.columns:
        bars.append(list(df2[config]))
    # for config in df.columns:
    #     bars2.append(list(df[config]))

    # Set position of bar on X axis
    r1 = np.arange(len(bars[0]))
    r2 = [x + barWidth for x in r1]

    # Make the plot
    plt.bar(r1, bars[0], color='#7f6d5f', width=barWidth,
            edgecolor='white', label=df2.columns[0])
    plt.bar(r2, bars[1], color='#557f2d', width=barWidth,
            edgecolor='white', label=df2.columns[1])

    # plt.bar(r1, bars2[0], color='red', width=barWidth, edgecolor='white', label="a")
    # plt.bar(r2, bars2[1], color='blue', width=barWidth, edgecolor='white', label="b")

    # Add xticks on the middle of the group bars
    plt.ylabel("average script usage per file", fontweight='bold')
    plt.xlabel('configuration', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars[0]))], list(df.index))
    plt.xticks(rotation=45)
    plt.legend()
    return plt


def code_with_comments(data, xcol, ycol, cat="config"):
    plt.rc(({'font.size': 2}))

    fig, axs = plt.subplots(3, 3)
    i = 0
    j = 0

    for c in data[cat].value_counts().head(9).index:
        p = (i, j)
        git = data[data[cat] == c]
        x = git[xcol]
        y = git[ycol]
        axs[p].scatter(x, y, 0.5)
        b, m = polyfit(x, y, 1)
        axs[p].plot(x, b + m * x, '-', color="red",
                    alpha=0.25, scalex=False, scaley=False)
        axs[p].plot(np.array(range(x.max())), np.array(
            range(x.max())), '-', color="green", alpha=0.25)
        axs[p].set_title("{} (sample: {})".format(c, len(git)), fontsize=6)
        # axs[p].set_ylim(-1, 1200)
        # axs[p].set_xlim(0, 7000)

        # axs[i].xlabel("comments")
        # axs[i].xlabel("code")
        if j == 2:
            j = 0
            i += 1
        else:
            j += 1

    axs[(1, 0)].set(ylabel=ycol)
    axs[(2, 1)].set(xlabel=xcol)

    plt.rc(({'font.size': 2}))

    plt.show()
    pass


def get_last_timeframe(sorted_data, key, search):
    temp = sorted_data[(sorted_data[key] != "0") & (sorted_data[key] != 0)]
    temp[key] = pd.to_datetime(temp[key])
    temp = temp.sort_values(by=key, ascending=True).set_index(key)
    return temp.last(search)


def comparison(data, col, val, old_data=False):
    if col is None:
        return data

    if val is None:
        return data

    if isinstance(val, str) and old_data:
        return data[data[col] == "b'{}'".format(val)]

    return data[data[col] == val]


def get_last_years_ci_usage(sorted_data, data, col=None, col2=None, val=None, commit_n=1,r=None,all=True):
    export = []
    print("Searching for the last 5 years for {} {}".format(
        val, len(comparison(data, col2, val, True))))
    ci = 0
    total = 0

    if r is None:
        r = range(6, 5*12, 6)

    for i in r:
        temp_ci = comparison(get_last_timeframe(
            sorted_data, "commit_{}".format(commit_n), "{}M".format(i)), col, val)["id"].nunique() - ci
        temp_total = len(comparison(get_last_timeframe(
            data, "recent_commit{}".format(commit_n), "{}M".format(i)), col2, val, True)) - total
        ci += temp_ci
        total += temp_total
        if temp_total > 0:
            export.append({"time":i, "total": temp_total, "ci": temp_ci, "perc":temp_ci/temp_total*100})
            print("month: {} total: {} ci: {} perc: {}".format(
                i, temp_total, temp_ci, temp_ci/temp_total*100))
        else:
            print("month: {} no data")
    
    if all:
        ci = comparison(sorted_data, col, val)["id"].nunique() - ci
        total = len(comparison(data, col2, val, True)) - total
        print("total: {} ci: {} perc: {} (older than 5 years)".format(
        total, ci, ci/total*100))

        export.append({"time": "all", "total": total, "ci": ci, "perc":ci/total*100})
    
    return export


def get_commit_graphs(sorted_data, orginal_data):
    # for i in [1,2,3]:
    #         data = get_last_years_ci_usage(sorted_data, orginal_data, "lang", "language", commit_n=i)
    #         plt.plot([k["time"] for k in data], [k["perc"] for k in data], label="prev {} commit".format(i))

    # plt.xlabel("time")
    # plt.xticks(rotation=45)

    # plt.ylabel("percentage CI usage")
    # plt.legend()
    # save_as_pdf(plt, "last 5 years of commits sampled every 2 months (including older commits at the end)")


    # for i in [1,2,3]:
    #     data = get_last_years_ci_usage(sorted_data, orginal_data, "lang", "language", commit_n=i,r=range(1,2*3*12,2), all=False)
    #     plt.plot([k["time"] for k in data], [k["perc"] for k in data], label="prev {} commit".format(i))

    # plt.xlabel("time")
    # plt.xticks(rotation=45)

    # plt.ylabel("percentage CI usage")
    # plt.legend()
    # save_as_pdf(plt, "last 3 years of commits sampled every 2 months")

    for lang in ["JavaScript","Python", "TypeScript", "Go", "C++", "Java","Rust", "PHP", "Ruby", "C"]:
        print("getting data for the last 12 months for: {}".format(lang))   
        data = get_last_years_ci_usage(sorted_data, orginal_data, "lang","language", lang, r=range(1,7,1),all=False)
        data.reverse()
        plt.plot([k["time"] for k in data], [k["perc"] for k in data], label="{}".format(lang))


    # data = get_last_years_ci_usage(sorted_data, orginal_data, None, None)
    # plt.plot([k["time"] for k in data], [k["perc"] for k in data], label="all")
    plt.xlabel("time")
    plt.ylabel("percentage CI usage")
    plt.xticks(rotation=45)
    plt.rc(({'font.size': 5}))

    plt.legend()

    save_as_pdf(plt, "test lang corrected")

def main(experimenting, name1, name2, image_encoding, output="."):
    if experimenting:
        # data = csvReader.readfile("combined1.csv")
        # sorted_data = csvReader.readfile("yaml threaded6.csv")
        # spread_of_data_v2(data, sorted_data).show()
        # plt.clf()
        # spread_of_data_line_sub(data, sorted_data).show()
        # save_as_pdf(language_type(load_dataframe(name1), sorted_data), f"{output}/languages", image_encoding)
        # languages_table_topn(f"{output}/languages table.tex", 20, load_dataframe(name1), sorted_data)
        # langs = languages_table_topn(f"{output}/languages table.tex", 30, load_dataframe(name1), sorted_data)
        # save_as_pdf(popularity_vs_percentage_CI_scatter(langs, sorted_data), f"{output}/languages-scatter-CI",
        #             image_encoding)
        # save_as_pdf(config_topn(sorted_data, 20), f"{output}/config-topn", image_encoding)
        # langs = languages_table_topn(f"{output}/languages table.tex", 30, load_dataframe(name1), sorted_data)
        # save_as_pdf(popularity_vs_percentage_CI_scatter(langs, sorted_data), f"{output}/languages-scatter-CI",
        #             image_encoding)
        # code_with_comments(sorted_data, "code", "comments")
        # code_with_comments(sorted_data, "code", "file_lines")
        # code_with_comments(sorted_data, "code", "blank_lines")
        # code_with_comments(sorted_data, "single_line_comment", "multi_line_comment")
        # code_with_comments(sorted_data, "multi_line_comment", "multi_line_comment_unique")
        #
        # code_with_comments(sorted_data, "code", "comments", "lang")
        # code_with_comments(sorted_data, "code", "file_lines", "lang")

        # save_as_pdf(line_usage_configuration(sorted_data[sorted_data["yaml"]]).show()
        # save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"]]).show()
        # save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"] == False]).show() asfdasdfasdfafdasdfasdfasdfasdfsdf
        # comment_uage_tbale(sorted_data)

        # save_as_pdf(line_usage_configuration(sorted_data), f"{output}/line structure all", image_encoding)
        # save_as_pdf(line_usage_configuration(sorted_data[sorted_data["yaml"]]), f"{output}/line structure yaml",
        #             image_encoding)
        # save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"]]),
        #             f"{output}/line structure yaml comments", image_encoding)
        # save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"] == False]),
        #             f"{output}/line structure none yaml comments", image_encoding)
        #
        # # data = csvReader.readfile(name1)
        # # #
        # # save_as_pdf(spread_of_data_sub_to_stars(data), f"{output}/sub vs stars", image_encoding)
        # scripts_latex(f"{output}/scripts table new.tex", sorted_data)
        # save_as_pdf(script_usage(sorted_data), f"{output}/scripts usage bars", image_encoding)

        # save_as_pdf(lines_against_scripts(sorted_data[sorted_data["yaml"]]), f"{output}/scripts vs lines", image_encoding)
        # save_as_pdf(stars_against_lines(sorted_data), f"{output}/scripts vs stars", image_encoding)
        sorted_data = load_dataframe(name2)
        orginal_data = pd.read_csv("2020 combined.csv", dtype={"id": int, "language": str}, parse_dates=[
                           "recent_commit1", "recent_commit2", "recent_commit3"])
        
        
        get_commit_graphs(sorted_data, orginal_data)
        # commit_n = 1
        # points = []
        # total = len(orginal_data)
        # for i in range(1,90):
        #     points.append((i, len(get_last_timeframe(orginal_data, "recent_commit{}".format(commit_n), "{}M".format(i)))/total*100))
        
        # plt.xticks(rotation=90)
        
        # plt.plot(["{}M".format(v[0]) for v in points], [v[1] for v in points])
        # save_as_pdf(plt, "test most recent question")

        

        # get_last_years_ci_usage(sorted_data, data, "lang", "language", commit_n=2)
        # get_last_years_ci_usage(sorted_data, data, "lang", "language", commit_n=3)

        # recent_commit1 = get_last_timeframe(data, "recent_commit1", "12M")
        
        # print("There are {} repositories that had their last commit in the last year. This is {} percentage of the total sample size.".format(len(recent_commit1), len(recent_commit1)/len(data)*100))
        # print("Out of all the last commits {} had CI".format(len(commit1)/len(recent_commit1)*100))

        # ci_two_years = len(get_last_timeframe(sorted_data, "commit_1", "2Y")) - len(commit1)
        # total_two_years = len(get_last_timeframe(data, "recent_commit1", "2Y")) - len(recent_commit1)

        # print("Out of all the last commits {} had CI".format(ci_two_years/total_two_years*100))

        # # # save_as_pdf(ci_usage_against_commits(data, sorted_data), f"{output}/cats", image_encoding)

        # # RQ3
        # langs = languages_table_topn(f"{output}/2019 languages table.tex", 30, load_dataframe(name1), sorted_data)
        # save_as_pdf(popularity_vs_percentage_CI_scatter(langs, sorted_data), f"{output}/2019-languages-scatter-CI",
        #             image_encoding)

    else:
        data = csvReader.readfile(name1)
        # #
        save_as_pdf(spread_of_data_sub_to_stars(data),
                    f"{output}/sub vs stars", image_encoding)
        save_as_pdf(spread_over_time_stars(data),
                    f"{output}/spread over time", image_encoding)
        save_as_pdf(spread_data_issues_vs_stars(data),
                    f"{output}/issues vs stars", image_encoding)

        sorted_data = load_dataframe(name2)
        yaml_config_errors_to_latex(
            f"{output}/yaml config errors.tex", sorted_data)
        # should not need to rerun this unless more scraping is done!!!
        # commented out as manual edits to the formatting are easier than code ones atm
        # config_type_split(f"{output}/configuration type count.tex", sorted_data)

        save_as_pdf(config_topn(sorted_data, 20),
                    f"{output}/config-topn", image_encoding)

        # RQ3
        langs = languages_table_topn(
            f"{output}/languages table.tex",
            30,
            pd.read_csv(name1,
                        dtype=dtypes,
                        parse_dates=["recent_commit1", "recent_commit2", "recent_commit3"]),
            sorted_data)
        save_as_pdf(popularity_vs_percentage_CI_scatter(langs, sorted_data), f"{output}/languages-scatter-CI",
                    image_encoding)

        save_as_pdf(langues_topn(sorted_data, 30),
                    f"{output}/languages-topn", image_encoding)

        save_as_pdf(language_type(pd.read_csv(name1, dtype=dtypes,parse_dates=[ "recent_commit1", "recent_commit2", "recent_commit3"]), sorted_data), f"{output}/languages", image_encoding)

        # --------------
        sorted_data_csv = csvReader.readfile(name2)
        save_as_pdf(spread_of_data_line_star(data, sorted_data_csv), f"{output}/percentage stars with CI",
                    image_encoding)
        save_as_pdf(spread_of_data_line_sub(data, sorted_data_csv),
                    f"{output}/percentage sub with CI", image_encoding)
        save_as_pdf(spread_of_data_line_star_other_paper(), f"{output}/percentage sub with CI other paper source",
                    image_encoding)

        # render_sankey_diagram.save_sanky_daigram_for_errors_and_comments(f"./{output}/sankey",
        #                                                                  pd.read_csv(name2, dtype=dtypes), False, False,
        #                                                                  image_encoding)
        # render_sankey_diagram.save_sanky_daigram_for_errors_and_comments(f"./{output}/sankey2",
        #                                                                  pd.read_csv(name2, dtype=dtypes), False, True,
        #                                                                  image_encoding)
        # render_sankey_diagram.save_sanky_daigram_for_errors_and_comments(f"./{output}/sankey3",
        #                                                                  pd.read_csv(name2, dtype=dtypes), True, False,

        save_as_pdf(line_usage_configuration(sorted_data),
                    f"{output}/line structure all", image_encoding)
        save_as_pdf(line_usage_configuration(sorted_data[sorted_data["yaml"]]), f"{output}/line structure yaml",
                    image_encoding)
        save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"]]),
                    f"{output}/line structure yaml comments", image_encoding)
        save_as_pdf(line_usage_configuration2(sorted_data[sorted_data["yaml"] == False]),
                    f"{output}/line structure none yaml comments", image_encoding)

        save_as_pdf(comment_usage(sorted_data),
                    f"{output}/comments usage bars", image_encoding)

        save_as_pdf(script_usage(sorted_data),
                    f"{output}/scripts usage bars", image_encoding)
        scripts_latex(f"{output}/scripts table new.tex", sorted_data)
        save_as_pdf(lines_against_scripts(sorted_data),
                    f"{output}/scripts vs lines", image_encoding)
        save_as_pdf(stars_against_lines(sorted_data),
                    f"{output}/scripts vs stars", image_encoding)

    return sorted_data


if __name__ == '__main__':
    # data = main(True, "2019 combined.csv", "2019 yaml threaded.csv", "pdf", "./results")
    data = main(True, "2020 combined.csv",
                "2020 yaml threaded5.csv", "pdf", "./results")
    # data = main(False, "combined9.csv", "yaml threaded14.csv", "svg", "./results")
    # main(True, "combined1.csv", "yaml threaded6.csv", "svg", "./results")
