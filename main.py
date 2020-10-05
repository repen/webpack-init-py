from subprocess import check_output, CalledProcessError
import logging, json, pathlib, os


logging.basicConfig(format='%(asctime)s : line %(lineno)-3s : %(name)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


logger = logging.getLogger(__name__)
CURRENT_DIR = os.getcwd()

temp_file_01 = '''
"use strict";


import { Hello } from "./module/hello_world.js";

console.log("Main load");

Hello.call();
'''.strip()

temp_file_02 = '''
"use strict";

let Hello = {
    call : function(){
        console.log("This module hello world!!!");
    }
};

export { Hello };
'''.strip()

temp_file_03 = '''
body {
    background-color: #706F6F;
}
'''.strip()

temp_file_04 = '''
@import 'style/custom.scss'
'''.strip()

config_webPack = '''
module.exports = {
    entry: './js/main.js',
    output: {
        filename: './bundle.js'
    }
};
'''.strip()

def run_cmd(cmd):
    try:
        out_bytes = check_output(cmd, shell=True)
        logger.info("\n%s", out_bytes.decode())
    except CalledProcessError as e:
        logger.info("%s %s", e.returncode, e.output)



cmd1 = "npm init --yes"
cmd2 = "npm install --save-dev webpack webpack-cli"
cmd3 = "npm install --save sass"


def add_cmd_package():
    with open("package.json") as f:
        data = json.load(f)
    data['scripts']["start"] = "webpack -d"
    data['scripts']["watch"] = "webpack -d --watch"
    
    data['scripts']["style"]     = "sass --no-source-map style/base.scss:style/style.min.css"
    data['scripts']["wstyle"]    = "sass style/base.scss style/style.min.css --watch"
    data['scripts']["style-min"] = "sass style/base.scss style/style.min.css --style compressed"


    with open("package.json", "w") as f:
        json.dump(data, f)
    logger.info("update package.json \n %s", data)

def create_config_wp():
    with open("webpack.config.js", "w") as f:
        f.write(config_webPack)


def create_structure_dir():
    a = os.path.join(CURRENT_DIR, "js/module")
    b = os.path.join(CURRENT_DIR, "dist")
    c = os.path.join(CURRENT_DIR, "style/style")
    fs = [a,b,c]
    for d in fs:
        pathlib.Path(d).mkdir(parents=True, exist_ok=True)
    logger.info("Structure dir created")

def create_files():
    mainjs      = ( os.path.join(CURRENT_DIR, "js/main.js"), temp_file_01 )
    hello_world = ( os.path.join(CURRENT_DIR, "js/module/hello_world.js"), temp_file_02 )
    customstyle = ( os.path.join(CURRENT_DIR, "style/style/custom.scss"), temp_file_03 )
    basesccs    = ( os.path.join(CURRENT_DIR, "style/base.scss"), temp_file_04 )
    files = [mainjs, hello_world, customstyle, basesccs]
    for fl in files:
        with open(fl[0], "w") as f:
            f.write(fl[1])
        logger.info("file: %s created", fl[0])


run_cmd(cmd1)
run_cmd(cmd2)
run_cmd(cmd3)
add_cmd_package()
create_config_wp()
create_structure_dir()
create_files()