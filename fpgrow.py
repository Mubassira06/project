#Function to load file and return lists of Transactions

# importing the library
from memory_profiler import profile
import time
from memory_profiler import profile
def Load_data(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    Transaction = []
    for i in range(0, len(content)):
        Transaction.append(content[i].split())
    return Transaction

#To convert initial transaction into frozenset
def create_initialset(dataset):  #avoiding duplicate rows
    retDict = {}

    for trans in dataset:
        #print(trans)
        retDict[tuple(trans)] = 1
    #print(retDict)
    length=len(retDict)
    return length,retDict

class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def increment_counter(self, counter):
        self.count += counter
@profile
def create_FPTree(dataset, minSupport):
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction: #1 2 3
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
            #print(dataset[transaction],"hel")
    #print(HeaderTable)
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del(HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]
     # 5 - [5,None]
    retTree = TreeNode('Null Set',1,None)

    for itemset,count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
                #3 5 = 5
        if len(frequent_transaction) > 0:
            ordered_itemset = []
            sorted_items = sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)
            #print(sorted_items)
            for v in sorted_items:
              ordered_itemset.append(v[0])
            #to update the FPTree

            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable

#To create the FP Tree using ordered itemsets
def updateTree(itemset, FPTree, HeaderTable, count):
   
    if itemset[0] in FPTree.children:     
        FPTree.children[itemset[0]].increment_counter(count)
    else:     
        new_node = TreeNode(itemset[0], count, FPTree)
        FPTree.children[itemset[0]] = new_node

        if HeaderTable[itemset[0]][1] is None:
            HeaderTable[itemset[0]][1] = new_node
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], new_node)
    if len(itemset) > 1:
        updateTree(itemset[1:], FPTree.children[itemset[0]], HeaderTable, count)


#To update the link of node in FP Tree
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node


def FPTree_uptransveral(leaf_Node, prefixPath):
 if leaf_Node.parent != None:
    prefixPath.append(leaf_Node.name)
    FPTree_uptransveral(leaf_Node.parent, prefixPath)


def find_prefix_path(basePat, TreeNode):
    Conditional_patterns_base = {}

    while TreeNode is not None:
        prefixPath = []
        FPTree_uptransveral(TreeNode, prefixPath)
        if len(prefixPath) > 1:
            conditional_set = set(prefixPath[1:])  
            Conditional_patterns_base[tuple(conditional_set)] = TreeNode.count 
            #print(TreeNode.name,TreeNode.count,'helo')
        TreeNode = TreeNode.nodeLink

    return Conditional_patterns_base

class pattern:
  def __init__(self,iset,s):
    self.itemset=iset.copy()
    self.support=s

def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = []
    pettern_len=[]
    pairs = HeaderTable.items()
    pattern_lengths=[]
     #itemset_frozen = frozenset(itemset)
    

    sorted_pairs = sorted(pairs, key=lambda p: p[1][0])

    for v in sorted_pairs:
      key, _ = v  # Extract the key (we don't need the value here) 
   
      bigL.append(key)  
   
    for basePat in bigL:  #
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        # Add frequent itemset to final list of frequent itemsets
        support = HeaderTable[basePat][1].count
        #print(support)
        pattern_lengths.append((new_frequentset, support))
       # print(new_frequentset)
        
        frequent_itemset.append(new_frequentset)
        #pattern_lengths.setdefault(len(new_frequentset), 0)

        
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases, minSupport)
        if Conditional_header is not None:
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)
    return pattern_lengths

def print_tree2(node, indent='', last_child=False):
  if node is not None:
    node_str = f"{node.name} ({node.count})"
    branch = "└─ " if last_child else "├─ "
    print(indent + branch + node_str)
    indent += "    " if last_child else "│   "
    children = list(node.children.values())
    for i, child in enumerate(children):
      is_last = i == len(children) - 1
      print_tree2(child, indent, is_last)

def write_tree_to_file(node, file, indent='', last_child=False):
  if node is not None:
    node_str = f"{node.name} ({node.count})"
    branch = "└─ " if last_child else "├─ "
    file.write(indent + branch + node_str + '\n')
    indent += "    " if last_child else "│   "
    children = list(node.children.values())
    for i, child in enumerate(children):
      is_last = i == len(children) - 1
      write_tree_to_file(child, file, indent, is_last)

def write_tree(names):
  filename = names
  with open(filename, 'w') as file:
    write_tree_to_file(FPtree, file)

def print_support_counts(frequent_itemset, HeaderTable):
    for itemset in frequent_itemset:
        support_count = min(HeaderTable[item][0] for item in itemset)
        print(f"Support Count of {itemset}: {support_count}")


filename = "D:\Coding\My_codes\CSE 477\Cse-477-Project\data.txt"
write_file="output_tree.txt"
length,initSet = create_initialset(Load_data(filename))
min_Support = (50/100)*length

start = time.time()


FPtree, HeaderTable = create_FPTree(initSet, min_Support)
frequent_itemset = []
txt=Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)
end = time.time()

print("Time Taken:")
print(end-start)
print("All frequent itemsets:")
frequent_itemset = sorted(frequent_itemset, key=lambda x: len(x))
for i in frequent_itemset:
  print(i)

#print_tree2(FPtree)
write_tree(write_file)
#print(txt)