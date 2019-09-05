"""
说明：这是对于无路段关联可靠最短路问题的一个简单算例。只有两条路径，为了简化程序，直接输入两条路径的均值和方差。
path,mean,var
0,35,0
1,29,49
"""
def main():
    #Step1 初始化
    path_list=[0,1]
    path_mean=[35,29]
    path_var=[0,49]
    beta=1     #可靠度系数
    delta=0.01 #可接受误差
    K=50       #迭代次数
    iteration=0
    gap=0
    multiplier=1 #初始化乘子
    #初始化上下界
    UB_global=float("inf")
    LB_global=-float("inf")
    #求解最小期望路径问题
    shortest_path_index=path_mean.index(min(path_mean))
    #设置最小期望路径对应得方差为y_的值;最小期望路径代入原问题得上界值
    y_=path_var[shortest_path_index]
    UB_global=min(path_mean)+y_**0.5
    #记录乘子大小
    multiplier_list=[]


    while iteration<K:
        #Step2 求解子问题1和2
        #1.广义成本最短路
        path_with_new_cost=[]
        for path in range(len(path_mean)):
            path_new_cost=path_mean[path]+multiplier*path_var[path]
            path_with_new_cost.append(path_new_cost)
        sub_problem_object1=min(path_with_new_cost)
        shortest_path_index=path_with_new_cost.index(sub_problem_object1)

        #2.单变量凹问题
        sub_problem_object2=min(0,beta*y_**0.5-multiplier*y_)
        #得到y得值
        if sub_problem_object2==0:
            y=0
        else:
            y=y_

        #更新下界值
        object_value=sub_problem_object1+sub_problem_object2
        LB_global=max(LB_global,object_value)

        #更新上界值：可行解代入目标函数
        UB_local=path_mean[shortest_path_index]+path_var[shortest_path_index]**0.5
        if UB_global>UB_local:
            UB_global=UB_local
            reliable_path_index=shortest_path_index

        #更新gap值
        gap=(UB_global-LB_global)/UB_global
        iteration+=1
        # if gap > delta:
        #     break

        #Step3：更新乘子
        multiplier_list.append(multiplier)
        multiplier=multiplier+(UB_global-object_value)/(path_var[shortest_path_index]-y)

    # print(iteration)
    # print(gap)
    print(multiplier_list)
    print("最可靠路径为{}，其目标值为{},gap值为{}".format(reliable_path_index,UB_global,gap))






if __name__ == '__main__':
    main()