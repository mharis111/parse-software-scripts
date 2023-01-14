
import ast
from parse_code import parse_ast
from csv import DictReader
from csv import writer
import os
from zipfile import ZipFile
import zipfile
from analyzeCode import extract_datasets

res=[]

def read_data(repo_name):
    if not (repo_name.endswith('.zip') or repo_name.endswith('.ZIP') or repo_name.endswith('.Zip')):
        return []
    name='downloadedFiles/'+repo_name
    print('name', name)
    files = []
    try:
        with ZipFile(name, 'r') as zipObject:
            with zipfile.ZipFile(name) as zfile:
                zfile.extractall('temp')
                listOfFileNames = zipObject.namelist()
                for fileName in listOfFileNames:
                    if fileName.endswith('.py') or fileName.endswith('.PY'):
                        files.append('temp/'+fileName)
                        #with open('temp/'+fileName) as f:
                        #print(open('temp/'+fileName).read())
    except:
        print("extracting error")
    return files
    
def parse_scripts(files):
    for f in files:
        script = open(f, encoding="ISO-8859-1").read()
        print('file',  f)
        print("-------------")
        try:
            res = parse_ast(script)
            print(res)
        except:
            print("cannot parsed")

def read_files():

    with open('data.csv', 'r', encoding="ISO-8859-1") as my_file:
     #passing file object to DictReader()
        csv_dict_reader = DictReader(my_file)
     #iterating over each row
        for i in csv_dict_reader:
            repo_name=i['name']
            head, tail = os.path.split(repo_name)
            files = read_data(repo_name)
            if len(files) > 0:
                parse_scripts(files)
                
                
    #res = parse_ast(SOURCE)
    #print(res)
def main():
    #read_files()
    script = """test_data = pd.read_csv("Sample.csv")
reference = pd.read_csv("Reference.csv")
train = reference.drop("MF_name",1)
test_data = test_data.drop("gene",1)

score_adj = []
for o in range(len(test_data.columns)):
    test = test_data.loc[:,test_data.columns[o]]
    im_name = train.columns
    svr = LinearSVR(random_state=0)
    model = svr.fit(train, test)
    score = model.coef_
    score[np.where(score<0)] = 0 
    score_adj.append((score/sum(score)))
score_adj = pd.DataFrame(score_adj)
score_adj.columns = im_name
score_adj.plot(kind='bar', stacked=True,legend=False)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.suptitle("Flow&Estimate")
plt.rcParams['figure.figsize'] = (6.69,8.86)
plt.rcParams['figure.dpi'] = 300
name = "bar.pdf"
plt.savefig(name,bbox_inches="tight" )
plt.close()
plt.boxplot(score_adj.T,patch_artist = True)
plt.suptitle("Flow&Estimate")
plt.xticks(range(8), im_name)
plt.rcParams['figure.figsize'] = (6.69,8.86)
plt.rcParams['figure.dpi'] = 300
name = "boxplot.pdf"
plt.savefig(name)

score_adj.to_csv("score.csv")
"""

    res = parse_ast(script)
    print("-------------")
    extract_datasets(res)
    script = """
def measuretime(f, n, *args):
    t = [0]*n
    res = f(*args)
    for n in range(n):
        t0 = time.time()
        f(*args)
        t[n] = time.time() - t0
    return(1000*np.array(t), res)
def fun_rqa(v,metric):
    # Attempt sparse RQA if metric is euclidean
    metric_sup = (metric is "supremum")
    rp = RecurrencePlot(v, metric=metric, sparse_rqa=metric_sup,
    threshold=1.2, dim=3, tau=6)
    rqa = rp.rqa_summary()
    rqa["Lmax"] = rp.max_diaglength()
    rqa["ENT"] = rp.diag_entropy()
    rqa["TT"] = rp.trapping_time()
    return(rqa)
    
def benchmark(metric):
    m = np.loadtxt("rossler.txt")
    for r in range(12):
        x = m[:250*(r+1), 2*r]
        (tt, res) = measuretime(fun_rqa, 5, x, metric)
        t = median(tt)
        with open("benchmark_rqa_python_%s.txt"%metric, "a") as f:
            f.write("%d\t%f\t"%(r,t))
            for k in ["RR","DET","L","Lmax","ENT","LAM","TT"]:
                f.write("%s\t"%(res[k]))
                f.write("\\n")
    """
    res = parse_ast(script)
    print("--------------")
    extract_datasets(res)
    #download_zenodo_repositories()
    #download_selected_files()
    #get_python_R_packages()


if __name__ == "__main__":
    main()