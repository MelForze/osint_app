import subprocess


def subfinder(scope):
    try:
        count_pos = 0
        new_result = []
        print("Domain: " + scope + " start!")
        result = subprocess.check_output(
            ["subfinder", "-d", scope, "-silent", "-nW", "-oI"]).decode('utf-8').split('\n')
        if len(result) == 1 and result[0] == '':
            print("Поддоменов нет")
            print("Domain: " + scope + " complete!")
            return 0
        for i in range(len(result)-1):
            old_data = result[i].split(',')
            for new_data in old_data:
                new_result.append(new_data)
            old_data = []
        data = []
        for i in range(len(new_result)):
            count_pos += 1
            if count_pos == 3:
                count_pos = 0
            else:
                data.append(new_result[i])
        result = data
        try:
            w_scope = scope.replace('.', '_')
            file = open(w_scope + '.txt', "w")
        except:
            print("I can't create a file")
        stage = 0
        for variable in result:
            if stage == 0:
                file.write(variable + ",")
                stage += 1
            elif stage == 1:
                file.write(variable + "\n")
                stage = 0
        print("Domain: " + scope + " complete!")
    except:
        print("subfinder broke or not installed")
        print("Please check your system")
