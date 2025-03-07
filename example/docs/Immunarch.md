# Immunarch

Exploration of Single-cell and Bulk T-cell/Antibody Immune Repertoires

See https://immunarch.com/articles/web_only/v3_basic_analysis.html
See <https://google.com>
See <https://github.com>

After [`ImmunarchLoading`](./ImmunarchLoading.md) loads the raw data into an [immunarch](https://immunarch.com) object,
this process wraps the functions from [`immunarch`](https://immunarch.com) to do the following:<br />

- Basic statistics, provided by [`immunarch::repExplore`](https://immunarch.com/reference/repExplore.html), such as number of clones or distributions of lengths and counts.<br />
- The clonality of repertoires, provided by [`immunarch::repClonality`](https://immunarch.com/reference/repClonality.html)
- The repertoire overlap, provided by [`immunarch::repOverlap`](https://immunarch.com/reference/repOverlap.html)
- The repertoire overlap, including different clustering procedures and PCA, provided by [`immunarch::repOverlapAnalysis`](https://immunarch.com/reference/repOverlapAnalysis.html)
- The distributions of V or J genes, provided by [`immunarch::geneUsage`](https://immunarch.com/reference/geneUsage.html)
- The diversity of repertoires, provided by [`immunarch::repDiversity`](https://immunarch.com/reference/repDiversity.html)
- The dynamics of repertoires across time points/samples, provided by [`immunarch::trackClonotypes`](https://immunarch.com/reference/trackClonotypes.html)
- The spectratype of clonotypes, provided by [`immunarch::spectratype`](https://immunarch.com/reference/spectratype.html)
- The distributions of kmers and sequence profiles, provided by [`immunarch::getKmers`](https://immunarch.com/reference/getKmers.html)

## Environment Variable Design

With different sets of arguments, a single function of the above can perform different tasks. For example, `repExplore` can be used to get the statistics of the size of the repertoire, the statistics of the length of the CDR3 region, or the statistics of the number of the clonotypes. Other than that, you can also have different ways to visualize the results, by passing different arguments to the [`immunarch::vis`](https://immunarch.com/reference/vis.html) function. For example, you can pass `.by` to `vis` to visualize the results of `repExplore` by different groups.<br />

Before we explain each environment variable in details in the next section, we will give some examples here to show how the environment variables are organized in order for a single function to perform different tasks.<br />

```python
# Repertoire overlapping
[Immunarch.envs.overlaps]
# The method to calculate the overlap, passed to `repOverlap`
method = "public"
```


What if we want to calculate the overlap by different methods at the same time? We can use the following configuration:<br />

```toml
[Immunarch.envs.overlaps.cases]
Public = { method = "public" }
Jaccard = { method = "jaccard" }
```

Then, the `repOverlap` function will be called twice, once with `method = "public"` and once with `method = "jaccard"`. We can also use different arguments to visualize the results. These arguments will be passed to the `vis` function:<br />

```toml
[Immunarch.envs.overlaps.cases.Public]
method = "public"
vis_args = { "-plot": "heatmap2" }

[Immunarch.envs.overlaps.cases.Jaccard]
method = "jaccard"
vis_args = { "-plot": "heatmap2" }
```

`-plot` will be translated to `.plot` and then passed to `vis`. See also [Namespace and Environment Variables](../configurations.md#namespace-environment-variables).<br />

If multiple cases share the same arguments, we can use the following configuration:<br />

```toml
[Immunarch.envs.overlaps]
vis_args = { "-plot": "heatmap2" }

[Immunarch.envs.overlaps.cases]
Public = { method = "public" }
Jaccard = { method = "jaccard" }
```

For some results, there are futher analysis that can be performed. For example, for the repertoire overlap, we can perform clustering and PCA (see also <https://immunarch.com/articles/web_only/v4_overlap.html>):<br />

```R
imm_ov1 <- repOverlap(immdata$data, .method = "public", .verbose = F)
repOverlapAnalysis(imm_ov1, "mds") %>% vis()
repOverlapAnalysis(imm_ov1, "tsne") %>% vis()
```

In such a case, we can use the following configuration:<br />

```toml
[Immunarch.envs.overlaps]
method = "public"

[Immunarch.envs.overlaps.analyses.cases]
MDS = { "-method": "mds" }
TSNE = { "-method": "tsne" }
```

Then, the `repOverlapAnalysis` function will be called twice on the result generated by `repOverlap(immdata$data, .method = "public")`, once with `.method = "mds"` and once with `.method = "tsne"`. We can also use different arguments to visualize the results. These arguments will be passed to the `vis` function:<br />

```toml
[Immunarch.envs.overlaps]
method = "public"

[Immunarch.envs.overlaps.analyses]
# See: https://immunarch.com/reference/vis.immunr_hclust.html
vis_args = { "-plot": "best" }

[Immunarch.envs.overlaps.analyses.cases]
MDS = { "-method": "mds" }
TSNE = { "-method": "tsne" }
```

Generally, you don't need to specify `cases` if you only have one case. A default case will be created for you. For multiple cases, the arguments at the same level as `cases` will be inherited by all cases.<br />

## Input

- `immdata`:
    The data loaded by `immunarch::repLoad()`

## Output

- `outdir`: *Default: `{{in.immdata | stem}}.immunarch`*. <br />
    The output directory

## Envs

- `mutaters` *(`type=json;order=-9`)*: *Default: `{}`*. <br />
    The mutaters passed to `dplyr::mutate()` on `immdata$meta` to add new columns.<br />
    The keys will be the names of the columns, and the values will be the expressions.<br />
    The new names can be used in `volumes`, `lens`, `counts`, `top_clones`, `rare_clones`, `hom_clones`, `gene_usages`, `divs`, etc.<br />
- `volumes` *(`ns`)*:
    Explore clonotype volume (sizes).<br />
    - `by`:
        Groupings when visualize clonotype volumes, passed to the `.by` argument of `vis(imm_vol, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.volumes` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.volume.by`, `envs.volume.devpars`.<br />
- `lens` *(`ns`)*:
    Explore clonotype CDR3 lengths.<br />
    - `by`:
        Groupings when visualize clonotype lengths, passed to the `.by` argument of `vis(imm_len, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.lens` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.lens.by`, `envs.lens.devpars`.<br />
- `counts` *(`ns`)*:
    Explore clonotype counts.<br />
    - `by`:
        Groupings when visualize clonotype counts, passed to the `.by` argument of `vis(imm_count, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.counts` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.counts.by`, `envs.counts.devpars`.<br />
- `top_clones` *(`ns`)*:
    Explore top clonotypes.<br />
    - `by`:
        Groupings when visualize top clones, passed to the `.by` argument of `vis(imm_top, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `marks` *(`list;itype=int`)*: *Default: `[10, 100, 1000, 3000, 10000, 30000, 100000.0]`*. <br />
        A numerical vector with ranges of the top clonotypes. Passed to the `.head` argument of `repClonoality()`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.top_clones` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.top_clones.by`, `envs.top_clones.marks` and `envs.top_clones.devpars`.<br />
- `rare_clones` *(`ns`)*:
    Explore rare clonotypes.<br />
    - `by`:
        Groupings when visualize rare clones, passed to the `.by` argument of `vis(imm_rare, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `marks` *(`list;itype=int`)*: *Default: `[1, 3, 10, 30, 100]`*. <br />
        A numerical vector with ranges of abundance for the rare clonotypes in the dataset.<br />
        Passed to the `.bound` argument of `repClonoality()`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.rare_clones` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.rare_clones.by`, `envs.rare_clones.marks` and `envs.rare_clones.devpars`.<br />
- `hom_clones` *(`ns`)*:
    Explore homeo clonotypes.<br />
    - `by`:
        Groupings when visualize homeo clones, passed to the `.by` argument of `vis(imm_hom, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `marks` *(`ns`)*:
        A dict with the threshold of the half-closed intervals that mark off clonal groups.<br />
        Passed to the `.clone.types` arguments of `repClonoality()`.<br />
        The keys could be:<br />
        - `Rare` *(`type=float`)*: *Default: `1e-05`*. <br />
            the rare clonotypes
        - `Small` *(`type=float`)*: *Default: `0.0001`*. <br />
            the small clonotypes
        - `Medium` *(`type=float`)*: *Default: `0.001`*. <br />
            the medium clonotypes
        - `Large` *(`type=float`)*: *Default: `0.01`*. <br />
            the large clonotypes
        - `Hyperexpanded` *(`type=float`)*: *Default: `1.0`*. <br />
            the hyperexpanded clonotypes
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.hom_clones` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.hom_clones.by`, `envs.hom_clones.marks` and `envs.hom_clones.devpars`.<br />
- `overlaps` *(`ns`)*:
    Explore clonotype overlaps.<br />
    - `method` *(`choice`)*: *Default: `public`*. <br />
        The method to calculate overlaps.<br />
        - `public`:
            number of public clonotypes between two samples.<br />
        - `overlap`:
            a normalised measure of overlap similarity.<br />
            It is defined as the size of the intersection divided by the smaller of the size of the two sets.<br />
        - `jaccard`:
            conceptually a percentage of how many objects two sets have in common out of how many objects they have total.<br />
        - `tversky`:
            an asymmetric similarity measure on sets that compares a variant to a prototype.<br />
        - `cosine`:
            a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.<br />
        - `morisita`:
            how many times it is more likely to randomly select two sampled points from the same quadrat (the dataset is
            covered by a regular grid of changing size) then it would be in the case of a random distribution generated from
            a Poisson process. Duplicate objects are merged with their counts are summed up.<br />
        - `inc+public`:
            incremental overlaps of the N most abundant clonotypes with incrementally growing N using the public method.<br />
        - `inc+morisita`:
            incremental overlaps of the N most abundant clonotypes with incrementally growing N using the morisita method.<br />
    - `vis_args` *(`type=json`)*: *Default: `{}`*. <br />
        Other arguments for the plotting functions `vis(imm_ov, ...)`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `analyses` *(`ns;order=8`)*:
        Perform overlap analyses.<br />
        - `method`: *Default: `none`*. <br />
            Plot the samples with these dimension reduction methods.<br />
            The methods could be `hclust`, `tsne`, `mds` or combination of them, such as `mds+hclust`.<br />
            You can also set to `none` to skip the analyses.<br />
            They could also be combined, for example, `mds+hclust`.<br />
            See https://immunarch.com/reference/repOverlapAnalysis.html
        - `vis_args` *(`type=json`)*: *Default: `{}`*. <br />
            Other arguments for the plotting functions.<br />
        - `devpars` *(`ns`)*:
            The parameters for the plotting device.<br />
            - `width` *(`type=int`)*: *Default: `1000`*. <br />
                The width of the plot.<br />
            - `height` *(`type=int`)*: *Default: `1000`*. <br />
                The height of the plot.<br />
            - `res` *(`type=int`)*: *Default: `100`*. <br />
                The resolution of the plot.<br />
        - `cases` *(`type=json`)*: *Default: `{}`*. <br />
            If you have multiple cases, you can use this argument to specify them.<br />
            The keys will be the names of the cases.<br />
            The values will be passed to the corresponding arguments above.<br />
            If any of these arguments are not specified, the values in `envs.overlaps.analyses` will be used.<br />
            If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
            values of `envs.overlaps.analyses.method`, `envs.overlaps.analyses.vis_args` and `envs.overlaps.analyses.devpars`.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.overlaps` will be used.<br />
        If NO cases are specified, the default case will be added, with the key the default method and the
        values of `envs.overlaps.method`, `envs.overlaps.vis_args`, `envs.overlaps.devpars` and `envs.overlaps.analyses`.<br />
- `gene_usages` *(`ns`)*:
    Explore gene usages.<br />
    - `top` *(`type=int`)*: *Default: `30`*. <br />
        How many top (ranked by total usage across samples) genes to show in the plots.<br />
        Use `0` to use all genes.<br />
    - `norm` *(`flag`)*: *Default: `False`*. <br />
        If True then use proportions of genes, else use counts of genes.<br />
    - `by`:
        Groupings to show gene usages, passed to the `.by` argument of `vis(imm_gu_top, .by = <values>)`.<br />
        Multiple columns should be separated by `,`.<br />
    - `vis_args` *(`type=json`)*: *Default: `{}`*. <br />
        Other arguments for the plotting functions.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `analyses` *(`ns;order=8`)*:
        Perform gene usage analyses.<br />
        - `method`: *Default: `none`*. <br />
            The method to control how the data is going to be preprocessed and analysed.<br />
            One of `js`, `cor`, `cosine`, `pca`, `mds` and `tsne`. Can also be combined with following methods
            for the actual analyses: `hclust`, `kmeans`, `dbscan`, and `kruskal`. For example: `cosine+hclust`.<br />
            You can also set to `none` to skip the analyses.<br />
            See https://immunarch.com/articles/web_only/v5_gene_usage.html.<br />
        - `vis_args` *(`type=json`)*: *Default: `{}`*. <br />
            Other arguments for the plotting functions.<br />
        - `devpars` *(`ns`)*:
            The parameters for the plotting device.<br />
            - `width` *(`type=int`)*: *Default: `1000`*. <br />
                The width of the plot.<br />
            - `height` *(`type=int`)*: *Default: `1000`*. <br />
                The height of the plot.<br />
            - `res` *(`type=int`)*: *Default: `100`*. <br />
                The resolution of the plot.<br />
        - `cases` *(`type=json`)*: *Default: `{}`*. <br />
            If you have multiple cases, you can use this argument to specify them.<br />
            The keys will be the names of the cases.<br />
            The values will be passed to the corresponding arguments above.<br />
            If any of these arguments are not specified, the values in `envs.gene_usages.analyses` will be used.<br />
            If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
            values of `envs.gene_usages.analyses.method`, `envs.gene_usages.analyses.vis_args` and `envs.gene_usages.analyses.devpars`.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be used as the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.gene_usages` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.gene_usages.top`, `envs.gene_usages.norm`, `envs.gene_usages.by`, `envs.gene_usages.vis_args`, `envs.gene_usages.devpars` and `envs.gene_usages.analyses`.<br />
- `spects` *(`ns`)*:
    Spectratyping analysis.<br />
    - `quant`:
        Select the column with clonal counts to evaluate.<br />
        Set to `id` to count every clonotype once.<br />
        Set to `count` to take into the account number of clones per clonotype.<br />
        Multiple columns should be separated by `,`.<br />
    - `col`:
        A string that specifies the column(s) to be processed.<br />
        The output is one of the following strings, separated by the plus sign: "nt" for nucleotide sequences,
        "aa" for amino acid sequences, "v" for V gene segments, "j" for J gene segments.<br />
        E.g., pass "aa+v" for spectratyping on CDR3 amino acid sequences paired with V gene segments,
        i.e., in this case a unique clonotype is a pair of CDR3 amino acid and V gene segment.<br />
        Clonal counts of equal clonotypes will be summed up.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the plot.<br />
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the plot.<br />
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the plot.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{'By_Clonotype': Diot({'quant': 'id', 'col': 'nt'}), 'By_Num_Clones': Diot({'quant': 'count', 'col': 'aa+v'})}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If any of these arguments are not specified, the values in `envs.spects` will be used.<br />
        By default, a `By_Clonotype` case will be added, with the values of `quant = "id"` and `col = "nt"`, and
        a `By_Num_Clones` case will be added, with the values of `quant = "count"` and `col = "aa+v"`.<br />
- `divs` *(`ns`)*:
    Parameters to control the diversity analysis.<br />
    - `filter`:
        The filter passed to `dplyr::filter()` to filter the data for each sample before calculating diversity.<br />
        For example, `Clones > 1` to filter out singletons.<br />
        To check which columns are available, use `immdata$data[[1]] |> colnames()` in R.<br />
        You may also check quickly here:<br />
        https://immunarch.com/articles/v2_data.html#basic-data-manipulations-with-dplyr-and-immunarch
        To use the top 10 clones, you can try `rank(desc(Clones)) <= 10`
    - `method` *(`choice`)*: *Default: `gini`*. <br />
        The method to calculate diversity.<br />
        - `chao1`:
            a nonparameteric asymptotic estimator of species richness.<br />
            (number of species in a population).<br />
        - `hill`:
            Hill numbers are a mathematically unified family of diversity indices.<br />
            (differing only by an exponent q).<br />
        - `div`:
            true diversity, or the effective number of types.<br />
            It refers to the number of equally abundant types needed for the average proportional abundance of the types to equal
            that observed in the dataset of interest where all types may not be equally abundant.<br />
        - `gini.simp`:
            The Gini-Simpson index.<br />
            It is the probability of interspecific encounter, i.e., probability that two entities represent different types.<br />
        - `inv.simp`:
            Inverse Simpson index.<br />
            It is the effective number of types that is obtained when the weighted arithmetic mean is used to quantify
            average proportional abundance of types in the dataset of interest.<br />
        - `gini`:
            The Gini coefficient.<br />
            It measures the inequality among values of a frequency distribution (for example levels of income).<br />
            A Gini coefficient of zero expresses perfect equality, where all values are the same (for example, where everyone has the same income).<br />
            A Gini coefficient of one (or 100 percents) expresses maximal inequality among values (for example where only one person has all the income).<br />
        - `d50`:
            The D50 index.<br />
            It is the number of types that are needed to cover 50%% of the total abundance.<br />
        - `dxx`:
            The Dxx index.<br />
            It is the number of types that are needed to cover xx%% of the total abundance.<br />
            The percentage should be specified in the `args` argument using `perc` key.<br />
        - `raref`:
            Species richness from the results of sampling through extrapolation.<br />
    - `by`:
        The variables (column names) to group samples.<br />
        Multiple columns should be separated by `,`.<br />
    - `args` *(`type=json`)*: *Default: `{}`*. <br />
        Other arguments for `repDiversity()`.<br />
        Do not include the preceding `.` and use `-` instead of `.` in the argument names.<br />
        For example, `do-norm` will be compiled to `.do.norm`.<br />
        See all arguments at
        https://immunarch.com/reference/repDiversity.html
    - `order` *(`list`)*: *Default: `[]`*. <br />
        The order of the values in `by` on the x-axis of the plots.<br />
        If not specified, the values will be used as-is.<br />
    - `test` *(`ns`)*:
        Perform statistical tests between each pair of groups.<br />
        Does NOT work for `raref`.<br />
        - `method` *(`choice`)*: *Default: `none`*. <br />
            The method to perform the test
            - `none`:
                No test
            - `t.test`:
                Welch's t-test
            - `wilcox.test`:
                Wilcoxon rank sum test
        - `padjust` *(`choice`)*: *Default: `none`*. <br />
            The method to adjust p-values.<br />
            Defaults to `none`.<br />
            - `bonferroni`:
                one-step correction
            - `holm`:
                step-down method using Bonferroni adjustments
            - `hochberg`:
                step-up method (independent)
            - `hommel`:
                closed method based on Simes tests (non-negative)
            - `BH`:
                Benjamini & Hochberg (non-negative)
            - `BY`:
                Benjamini & Yekutieli (negative)
            - `fdr`:
                Benjamini & Hochberg (non-negative)
            - `none`:
                no correction.<br />
    - `separate_by`:
        A column name used to separate the samples into different plots. Only works for `raref`.<br />
    - `align_x` *(`flag`)*: *Default: `False`*. <br />
        Align the x-axis of multiple plots. Only works for `raref`.<br />
    - `align_y` *(`flag`)*: *Default: `False`*. <br />
        Align the y-axis of multiple plots. Only works for `raref`.<br />
    - `log` *(`flag`)*: *Default: `False`*. <br />
        Indicate whether we should plot with log-transformed x-axis using `vis(.log = TRUE)`. Only works for `raref`.<br />
    - `devpars` *(`ns`)*:
        The parameters for the plotting device.<br />
        - `width` *(`type=int`)*: *Default: `1000`*. <br />
            The width of the device
        - `height` *(`type=int`)*: *Default: `1000`*. <br />
            The height of the device
        - `res` *(`type=int`)*: *Default: `100`*. <br />
            The resolution of the device
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be used as the names of the cases.<br />
        The values will be passed to the corresponding arguments above.<br />
        If NO cases are specified, the default case will be added, with the name of `envs.div.method`.<br />
        The values specified in `envs.div` will be used as the defaults for the cases here.<br />
- `trackings` *(`ns`)*:
    Parameters to control the clonotype tracking analysis.<br />
    - `targets`:
        Either a set of CDR3AA seq of clonotypes to track (separated by `,`), or simply an integer to track the top N clonotypes.<br />
    - `subject_col`: *Default: `Sample`*. <br />
        The column name in meta data that contains the subjects/samples on the x-axis of the alluvial plot.<br />
        If the values in this column are not unique, the values will be merged with the values in `subject_col` to form the x-axis.<br />
        This defaults to `Sample`.<br />
    - `subjects` *(`list`)*: *Default: `[]`*. <br />
        A list of values from `subject_col` to show in the alluvial plot on the x-axis.<br />
        If not specified, all values in `subject_col` will be used.<br />
        This also specifies the order of the x-axis.<br />
    - `cases` *(`type=json;order=9`)*: *Default: `{}`*. <br />
        If you have multiple cases, you can use this argument to specify them.<br />
        The keys will be used as the names of the cases.<br />
        The values will be passed to the corresponding arguments (`target`, `subject_col`, and `subjects`).<br />
        If any of these arguments are not specified, the values in `envs.trackings` will be used.<br />
        If NO cases are specified, the default case will be added, with the name `DEFAULT` and the
        values of `envs.trackings.target`, `envs.trackings.subject_col`, and `envs.trackings.subjects`.<br />

