import dash
import numpy as np
import pandas as pd
from dash import dcc
from dash import html
from controllers import *
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import Flask, render_template, request,  jsonify

df = pd.read_excel("Data_base.xlsx")

server = Flask(__name__)


@server.route('/name')
def name():
    return render_template('../Frontend/CardCss/index.html')

@server.route('/filter')
def GET_FILTERED_STATISTICS():
    try:
        family = request.args.get('family')
        variable = request.args.get('variable')
        toRespond = famFilter(df,family,variable)
        if 'error' in toRespond:
            return jsonify({'message': 'Failed to filter data'}), 400 
        else:
            return jsonify(toRespond)
    except:
        return jsonify({'message': 'process failed within controller "famFilter()". '}), 500


layout = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title></title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <link href="https://fonts.cdnfonts.com/css/belgrano" rel="stylesheet">
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="Portada.css">
    <link rel="stylesheet" href="titulos.css">
    <link rel="stylesheet" href="Intro.css">
    <script src="https://unpkg.com/feather-icons"></script>
    <link rel="stylesheet" href="content.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    {%css%}

</head>

<body>
    <!-- Main div-->
    <div id='mainDiv'>

        <!--- Title card  --->
        <div class='cardPortada'>
            <!-- Card Header-->
            <div class='cardHeader grayHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo' style="margin-left: 7%;">
                    </div>
                    <div class="headerTxt">
                    </div>
                </div>
            </div>
            <!-- Card Content -->
            <div class="cardContent">
                <img src="https://lh4.googleusercontent.com/8sG-8di91x9olkSpOjfsjW6ONK0s5p7EOJUsMKVFeRmXPMEziWGWiSq2cDpTODA6CcA=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
                <div class="contentTextPortada">

                    <span class="textWhite" style="font-size: 9vw;">
                        Refrigeradores <br> Whirpool
                    </span>

                    <span class="textWhite" style="font-size: 3.5vw; ">
                        Un análisis sobre su consumo <br> energético , temperaturas y más.
                    </span>

                </div>
            </div>
        </div>

        <!-- Introducción -->
        <div class="cardRightImage">
            <div id="generalContentIntro">
                <div class="cardHeader">
                    <div class="logodiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo' style="margin-left: 7%;">
                    </div>
                    <div class="headerTxt">
                        <div id="introHeaderTextRows">
                            <span class="textWhite" style="font-size: 3vw ;">Comparativa costos Bimestral</span>
                            <span class="textWhite" style="font-size: 2vw ;"> Whirpool vs Industria</span>
                        </div>
                    </div>
                </div>

                <div id="introContent">
                    <div class="introContentChild">
                        <div class="iconDiv">
                            <i class="goldIcons" data-feather="dollar-sign"></i>
                        </div>
                        <div class="introtextdata">
                            <span class="textWhite" style="font-size: 1.4vw ;">Recibo de luz promedio:</span>
                            <span class="textYellow" style="font-size: 1.4vw ;"> $437 mxn </span>
                            <span class="textWhite" style="font-size: 1.4vw ;">(scielo.org, 2021)</span>
                        </div>
                    </div>

                    <div class="introContentChild">
                        <div class="iconDiv">
                            <i class="goldIcons" data-feather="zap"></i>
                        </div>
                        <div class="introtextdata">
                            <span class="textWhite" style="font-size: 1.4vw ;">Promedio Kwh/Bm</span>
                            <span class="textWhite" style="font-size: 1.34vw ;"> Refrigeradores promedio </span>
                            <span class="textWhite" style="font-size: 1.4vw ;"> <span class="textYellow"> 68.67</span> (
                                <span class="textYellow">$58.43 mxn</span>)</span>
                            <span class="textWhite" style="font-size: 1.4vw ;"> <span class="textYellow">13.37%</span>
                                del recibo</span>
                            <span class="textWhite" style="font-size: 1.4vw ;">(Energystar.gov,2022)</span>
                        </div>
                    </div>

                    <div class="introContentChild">
                        <div class="iconDiv">
                            <i class="goldIcons" data-feather="zap"></i>
                        </div>
                        <div class="introtextdata">
                            <span class="textWhite" style="font-size: 1.4vw ;">Promedio Kwh/Bm:</span>
                            <span class="textWhite" style="font-size: 1.4vw ;"> Refrigerador whirlpool: </span>
                            <span class="textWhite" style="font-size: 1.4vw ;"><span class="textYellow">62.48</span>
                                (<span class="textYellow">$53.17 mxn</span>)</span>
                            <span class="textWhite" style="font-size: 1.4vw ;"><span class="textYellow">12.16%</span>
                                del promedio</span>
                        </div>
                    </div>

                </div>

                <div id="introDisclaimer">
                    <spanc class="textWhite" style="font-size: 1.8vw; margin-left: 5vw;">Datos Bimestrales</span>

                </div>

            </div>
            <div id="lightsImageDiv">
                <img src="https://lh6.googleusercontent.com/rWO_ieaNHdHx5N3yJ_7MeLICoc6Ur40SW7u-4unINeYVYsvrdzYgd3ppVuwI-EwGBLU=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
            </div>


        </div>

        <!--CARD 1(QUE DATOS TENEMOS)-->
        <div class='cardTitles'>
            <!-- Card Header 1 -->
            <div class='cardHeader yellowHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh6.googleusercontent.com/PygddDSvmyMVJK2KO1eayyp3ytJ-UeCGzhVcIeJZDPMF4LJQjLU1t0MtlVqiNn9zN10=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                    </div>
                </div>
            </div>
            <!-- Card Content 1  -->
            <div class="cardTitlesContent ">
                <img src="https://lh4.googleusercontent.com/YAPUf2OH7J7w5kFMgD2K77y167GK_y00SCd8Hq06Z46s6GudD_rGa1kFnnZghEVMYqw=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
                <div class="titleCenterText">
                    <span class="textWhite" style="font-size: 8vw;">
                        ¿Qué Datos Tenemos?
                    </span>
                </div>
            </div>
        </div>

        <!--CARD 1.2(Nuestros Recursos)-->
        <div class='cardTitles'>
            <!-- Card Header 1.2 -->
            <div class='cardHeader yellowHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh6.googleusercontent.com/PygddDSvmyMVJK2KO1eayyp3ytJ-UeCGzhVcIeJZDPMF4LJQjLU1t0MtlVqiNn9zN10=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt12">
                        <span class="textBlack" style="font-size: 3vw;">
                            Nuestros Recursos</span>
                    </div>
                </div>
            </div>
            <!-- Card Content 1.2  -->
            <div class="cardTitlesContent ">
                <div id="generalContentCard12">
                    <div class="varsText">
                        <span class="textBlack" style="font-size: 5vw;">
                            Variables
                        </span>
                    </div>
                    <div id="twoValues">
                        <span class="textBlack" style="font-size: 2.5vw; margin-right: 4vw">
                            40 Columnas
                        </span>
                        <span class="textBlack" style="font-size: 2.5vw;">
                            512 Registros
                        </span>
                    </div>
                    <div class="varsText">
                        <span class="textBlack" style="font-size: 2.5vw;">
                            Agrupaciones por familia, <br> plataforma, y refrigerante.
                        </span>
                    </div>
                    <div class="varsText">
                        <span class="textBlack" style="font-size: 2.5vw;">
                            Datos de temperaturas, tiempo de <br> uso, metas de uso energético, etc.
                        </span>
                    </div>
                </div>
                <div id="generalContentCard13">
                    <i id="dbIcon" data-feather="database"></i>
                </div>
            </div>

        </div>
        <!--CARD 1.2(Variables relevantes)-->
        <div class='cardTitles'>
            <!-- Card Header 1.2 -->
            <div class='cardHeader yellowHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh6.googleusercontent.com/PygddDSvmyMVJK2KO1eayyp3ytJ-UeCGzhVcIeJZDPMF4LJQjLU1t0MtlVqiNn9zN10=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt12">
                        <span class="textBlack" style="font-size: 3vw;">
                            Variables Relevantes</span>
                    </div>
                </div>
            </div>
            <!-- Card Content 1.2  -->
            <div class="cardTitlesContent ">
                <div id="VRinnerWrap">
                    <div id="VarRelLeft">
                        <div id="VRCol">
                            <span class="textBlack" style="font-size: 4vw; margin-bottom: 20px;">
                                Familias</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                4W3G80 117</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                4W3G12 92</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                6w3n80 79</span>
                            <span></span>
                        </div>
                        <div id="VRCol">
                            <span class="textBlack" style="font-size: 4vw; margin-bottom: 10px;">
                                Temperaturas</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                RC|FC Average</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                RC|FC 1</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                RC|FC 2</span>
                            <span class="textBlack" style="font-size: 1.8vw; width: 53%; text-align: left;">
                                RC|FC 3</span>

                        </div>
                    </div>
                    <div id="VarRelRight">
                        <span class="textBlack" style="font-size: 3vw; margin-bottom: 10px;">
                            Energy Usage Kwh/day</span>
                        <span class="textBlack" style="font-size: 3vw; margin-bottom: 10px;">
                            %Run Time</span>
                        <span class="textBlack" style="font-size: 3vw; margin-bottom: 10px;">
                            Supplier</span>
                        <span class="textBlack" style="font-size: 3vw; margin-bottom: 10px;">
                            Refrigerant</span>
                        <span class="textBlack" style="font-size: 3vw; margin-bottom: 10px;">
                            E-STAR</span>
                    </div>
                </div>
            </div>
        </div>
        <!--CARD 2 (DATOS ATIPICOS Title)-->
        <div class='cardTitles'>
            <!-- Card Header 2 -->
            <div class='cardHeader navyHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                    </div>
                </div>
            </div>
            <!-- Card Content 2  -->
            <div class="cardTitlesContent ">
                <img src="https://lh5.googleusercontent.com/bJC_k5alXWD0qdGrs6_oc6_knU3FRoDDZ91RH3T0HFjWX76RgHKGIt2ZQZk1Sxj0Wp8=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
                <div class="titleCenterText">
                    <span class="textWhite" style="font-size: 8vw;">
                        Estadísticas
                    </span>
                </div>
            </div>
        </div>
        <!--CARD 2 (DATOS ATIPICOS Contenido)-->
        <div class='cardTitles'>
            <!-- Card Header 2 -->
            <div class='cardHeader navyHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                    </div>
                </div>
            </div>
            <!-- Card Content 2  -->
            <div class="cardTitlesContent ">
                <div id="atipicoWrapper">
                    <div id="atipicoLeft">
                        <div class="atipicoFilter">

                            <select id="selectFamily" class="form-select form-select-lg text-white" style="--bs-bg-opacity: 1; background-color: #53606E; 
                                font-size: 2vw;" aria-label="Default select example">
                                <option selected>Selecciona una Familia...
                                </option>>
                                <option value="4W3G80">4W3G80</option>
                                <option value="4W3G12">4W3G12</option>
                                <option value="6w3n80">6w3n80</option>
                                <option value="5w3n80">5w3n80</option>
                                <option value="6w3n80">6w3n80</option>
                                <option value="4w3n90">4w3n90</option>
                                <option value="4w3iG81">4w3iG81</option>
                                <option value="4w3n10">4w3n10</option>
                                <option value="4W3G90">4W3G90</option>
                                <option value="6w3g10">6w3g10</option>
                                <option value="0w3i10">0w3i10</option>
                            </select>
                            <br>
                            <select id="selectVariable" class="form-select form-select-lg text-white" style="--bs-bg-opacity: 1; background-color: #53606E; 
                                font-size: 2vw;" aria-label="Default select example">
                                <option selected>Selecciona una variable...
                                </option>
                                <option value="FC Temp Average A°F (M/M)">FC Temp Average First Position.</option>
                                <option value="RC Temp Average A°F (M/M)">RC Temp Average First Position. </option>
                                <option value="FC1 Temp A°F">FC1 First Position.</option>
                                <option value="FC2 Temp A°F">FC2 First Position.</option>
                                <option value="FC3 Temp A°F">FC3 First Position.</option>
                                <option value="RC1 Temp °F">RC1 First Position.</option>
                                <option value="RC2 Temp A°F">RC2 First Position.</option>
                                <option value="RC3 Temp A°F">RC3 First Position.</option>
                                <option value="% Run Time (M/M)"> Percentage Run Time First Position.</option>
                                <option value="% Below Rating Point"> Below Rating Point.</option>
                                <option value="Energy Consumed (kWh/yr)"> Energy Consumed (kWh/yr).</option>
                            </select>
                            <br>
                            <button id="submitBtn" type="button"
                                class="btn btn-secondary btn-lg btn-block">Submit</button>
                        </div>

                        <div id="atipicoEstDescrpitivo">
                            <span class="AtEstText textBlack">Elementos: <span class="AtEstText textBlack"
                                    id="count">0</span></span>
                            <span class="AtEstText textBlack">Promedio: <span class="AtEstText textBlack"
                                    id="mean">0</span></span>
                            <span class="AtEstText textBlack" >Moda: <span
                                    class="AtEstText textBlack" id="mode">0</span></span>
                            <span class="AtEstText textBlack">Mediana: <span class="AtEstText textBlack"
                                    id="mediana">0</span></span>
                            <span class="AtEstText textBlack">Desviación Estandar: <span class="AtEstText textBlack"
                                    id="std">0</span></span>
                        </div>
                    </div>
                    <div id="atipicoRight">
                        <div id="atipicosProportion">
                            <span class="textBlack atipicoDataSize">Rangos de Aceptación</span>
                            <span class="textBlack atipicoDataSize">Rangos: <span id="rango">N/A</span></span>
                            <span class="textYellow atipicoDataSize2"><span id="withinRange">0</span>/<span
                                    id="total">0</span></span>
                            <span class="textYellow atipicoDataSize2" ><span id="percentagewithin">0</span>%</span>
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <!--CARD 5 (CONCLUSIONES)-->
        <div class='cardTitles'>
            <!-- Card Header 5 -->
            <div class='cardHeader navyHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                    </div>

                </div>
            </div>
            <!-- Card Content 5  -->
            <div class="cardTitlesContent ">
                <img src="https://lh4.googleusercontent.com/PoFRBdfnGVNtReCAR3oYjeoj0ndGkOs-JleZ44j50FwArrSiRZdWJnNohyKAftnQwmU=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
                <div class="titleCenterText">
                    <span class="textWhite" style="font-size: 8vw;">
                        Conclusiones
                    </span>

                </div>

            </div>

        </div>
        <!-- Card Header 5.2 -->
        <div class="cardTitles">
            <div class='cardHeader navyHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt12">
                        <span class="textWhite" style="font-size: 3vw;"> Tendencias</span>
                    </div>
                </div>
            </div>
            <!-- Card Content 5  -->
            <div class="cardTitlesContent" style="height: 1080px;">
                <div id="tendenciasWrapper">
                    <div id="tendenciasContentGraphs">
                        {%app_entry%}
                    </div>
                </div>
            </div>
        </div>
        <!--CARD 6 (RECOMENDACIONES)-->
        <div class='cardTitles'>
            <!-- Card Header 6 -->
            <div class='cardHeader grayHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                    </div>

                </div>
            </div>
            <!-- Card Content 6  -->
            <div class="cardTitlesContent ">
                <img src="https://lh4.googleusercontent.com/8ogtEyK39ntRaedvm6r_b0TSjwNfeKW6ItICnXMqdQYVXoAdT2QugA76VnvwfXifsHI=w2400"
                    class="imgBackground1">
                <div class="imgBackground105">
                    <span></span>
                </div>
                <div class="titleCenterText">
                    <span class="textWhite" style="font-size: 8vw;">
                        Recomendaciones
                    </span>

                </div>

            </div>
        </div>
        <!-- Card Header 5.2 -->
        <div class="cardTitles ">
            <div class='cardHeader navyHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt12">
                        <span class="textWhite" style="font-size: 3vw;"> Recomendaciones</span>
                    </div>
                </div>
            </div>
            <!-- Card Content 5  -->
            <div class="cardTitlesContent ">
                <div id="recoWrapper">
                    <div id="recoLeftCol">
                        <div id="arrowsImgDiv">
                            <img id="arrowsImg"
                                src="https://lh5.googleusercontent.com/vvG84bY0FUFaZ8CbXDNfn6NUCC07FjNe2fMZ3mwC24FZuinboCpgERbs7iE2mg22aZY=w2400">
                        </div>
                        <div id="moneyRecoDiv">
                            <i class="goldIcons" style="width: 25vw; height: auto; " data-feather="dollar-sign"></i>
                        </div>
                    </div>
                    <div id="recoRightCol">
                        <div>
                            <ul>
                                <li><span class="textBlack" style="font-size: 3vw;">El consumo de Energía</span></li>
                                <li><span class="textBlack" style="font-size: 3vw;">Modelo de regresión con FC, RC y Run
                                        Time %</span></li>
                                <li><span class="textBlack" style="font-size: 3vw;">Optimización de Ecuación del
                                        modelo</span></li>
                            </ul>

                        </div>
                        <div>
                            <span class="textBlack" style="font-size: 4vw;">AHORRO PARA EL CLIENTE <i class="goldIcons"
                                    style="width: 4vw; height: auto; " data-feather="smile"></i></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--(DASHBOARDS)-->
        <div class='cardTitles'>
            <!-- Card Header  -->
            <div class='cardHeader grayHeader'>
                <div class="HeaderCols">
                    <div class="logoDiv">
                        <img src="https://lh3.googleusercontent.com/3EZ4BlUHcuCAYwCcsTH8uR5a502hKZ_6z_MgS1ltwlFu-kLQwrxBEdhq0Up6VKtZbBc=w2400"
                            alt="Whirpool logo" class='logo'>
                    </div>
                    <div class="headerTxt">
                        <span class="textWhite" style="font-size: 3vw;">
                            Dashboards</span>
                    </div>
                </div>
            </div>
            <!-- Card Content   -->
            <div class="cardTitlesContent ">
                <div id="atipicoWrapper">
                    <div class="dashboardLeft">
                        <button  onclick="window.location.href='http\:\/\/127.0.0.1:8051/';"type="button" class="btn btn-primary btn-lg dashbtn">Descriptivo</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="index.js" async defer></script>
    <script>feather.replace()</script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4"
        crossorigin="anonymous"></script> '
    {%config%}
    {%scripts%}
    {%renderer%}
</body>

</html>
"""

app = dash.Dash(__name__, assets_folder="../Frontend/CardsCss",
                server=server, index_string=layout,external_stylesheets=[dbc.themes.CERULEAN])
app.layout = \
dbc.Container\
([
      html.Br(), #Titulo
      dbc.Row([dbc.Col([html.H1('Trend Dashboard', className='text-center text primary, mb-3')])]),
      
      html.Br(),
      dbc.Row([ #Primera fila (Dropdowns)
      dbc.Col([dcc.Dropdown(id='Familia Dropdown',
                       options=[{'label': i,'value': i}
                                for i in df['Familia'].unique()],
                       placeholder = 'select a Family',
                       #value='4W3G80'
                       )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='Refrigerante Dropdown',
                       options=[{'label': i,'value': i}
                                for i in df['Refrigerant'].unique()],
                       placeholder = 'select a Refrigerant',
                       #value='R600'
                       )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='x_dropdown',
                            options=[{'label': i, 'value':i}
                                     for i in df.columns],
                            placeholder = 'Select an X Variable',
                            #value='FC3 Temp A°F'
                            )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='y_dropdown',
                            options=[{'label': i, 'value':i}
                                     for i in df.columns],
                            placeholder = 'select a Y Variable',
                            #value='FC2 Temp A°F'
                            )],
              width=3)
      ]), #Fin de primera fila
      
      html.Br(),
      dbc.Row([dbc.Col([dcc.Graph(id='regression', style={'height':550})],width=12)]),
      
      html.Br(),
      dbc.Row([
          dbc.Col([dcc.Graph(id='Count', style={'height':200})],width=6),
          dbc.Col([dcc.Graph(id='Corr', style={'height':200})],width=6)
          ])
])


@app.callback( #Grafica
    Output(component_id='regression', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value'),
    Input(component_id='y_dropdown', component_property= 'value')
)

def indicadores_pm(selected_family, selected_refrigerant, x_var, y_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    data = px.scatter(filtered_df, x=x_var,y=y_var,template = 'plotly_white', trendline='ols')
    
    return data

@app.callback( #Count
    Output(component_id='Count', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value')
)
def contador(selected_family, selected_refrigerant, x_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        value = filtered_df[x_var].count(),
        number = {"font":{"size":90}},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Number of Registries","font":{"size":20}}))
    
    return fig
@app.callback( #corr
    Output(component_id='Corr', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value'),
    Input(component_id='y_dropdown', component_property= 'value')
)

def corr(selected_family, selected_refrigerant, x_var, y_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    fig1 = go.Figure()

    fig1.add_trace(go.Indicator(
        value = np.corrcoef(filtered_df[x_var], filtered_df[y_var])[0,1],
        gauge = {
            'axis': {'visible': False}},
        number = {"font":{"size":90}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Pearson Correlation","font":{"size":20}}))
    
    return fig1

if __name__ == '__main__':
    app.run_server()