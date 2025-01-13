# Вы можете расположить сценарий своей игры в этом файле.

# Создание галереи
init python:
    g = Gallery()

    g.navigation = True
    g.span_buttons = True

    g.button('gallery')
    g.image('warning')
    g.transform(truecenter)
    g.image('big_dady')
    g.transform(truecenter)
    g.image('chill_gay')
    g.transform(truecenter)
    g.image('dream')
    g.transform(truecenter)
    g.image('frend_in_dark')
    g.transform(truecenter)
    g.image('lake')
    g.transform(truecenter)
    g.image('motomoto')
    g.transform(truecenter)
    g.image('soger_mazelov')
    g.transform(truecenter)
    g.image('update_drake')
    g.transform(truecenter)
    g.image('vova_poster')
    g.transform(truecenter)

# Работа с изображениями и звуками
init python:  

    # Переменная для хранения скорости текста
    text_speed = 20
    ts = text_speed # Сокращённое название

    # переменная для хранения имени говорящего
    speaking = None

    # степень яркости цветов, 1.0 - полноцвет
    opacity = 0.0

    #  Функция для выбора состояния спрайта - полноцвет/бледный
    def while_speaking(name, speak_d, st, at):
        if speaking == name:
            # цветной, если говорит в данный момент
            return speak_d, None
        else:
            # невидимый, если молчит (функция из модуля 7dots.rpy)
            done_d = At(speak_d, alpha(opacity))
            return done_d, None
    curried_while_speaking = renpy.curry(while_speaking)

    # для создания динамического изображения, состояние которого зависит от переменной
    def WhileSpeaking(name, speaking_d):
        return DynamicDisplayable(curried_while_speaking(name, speaking_d))

    # Функция для определения имени персонажа, который в данный момент что-то говорит
    # И создания эффекта "подёргивания" во время разговора
    # имя сохраняется в переменной speaking
    def speaker_callback(name, image_tag, event, interact=True, **kwargs):
        global speaking
        if event == "show":
            speaking = name
        elif event == "end":
            speaking = None

        showing_image = get_showing_images(image_tag)
        if event == "begin":
            renpy.show(showing_image, [breath(10/text_speed)])
        # elif event == "slow_done":
        #     renpy.show(showing_image, [breath(0.0, dz=0.0)])
        #     renpy.restart_interaction()

        if not interact:
            return

        if event == 'show_done':
            renpy.music.play(f'voice/{image_tag}.mp3', channel='vox', relative_volume=1.0)
        elif event == 'slow_done':
            renpy.music.stop(channel='vox')

    Speaker = renpy.curry(speaker_callback)

    # Функция для поиска названия отображаемого изображения с заданым тегом
    def get_showing_images(search_tag):
        
        #Записываем в переменную набор тегов изображений отображаемых на слое
        tags = renpy.get_showing_tags() 
        for tag_name in list(tags): 

            #Записываем в переменную упарядоченный список атрибутов изображения
            atrb = renpy.get_ordered_image_attributes(tag_name) 
            for a in atrb:
                
                # Искомое имя (тег+атибут)
                search_name = f'{tag_name} {a}'

                # Записываем условия в переменную
                cond1 = renpy.showing(search_name, layer='master')
                cond2 = tag_name == search_tag
                # Если оба условия верны записываем полное название в результат

                if cond1 and cond2:
                    result = search_name

        return result

    # Функция для создания всех изображения с одним тегом с динамическим изменением 
    def addAllImage(short_name, name):
        # Ищем в дериктории все пути нужной папки
        for path in renpy.list_files(True):
            # Какую папку ищем
            search_path = f'images/characters/{name}/'
            if search_path in path:
                # Вырезаем путь до папки, чтобы получить имя файла
                file_name = path.replace(search_path, '')
                # Вырезаем расширение файла
                change_name = file_name[:-4]
                image_name = change_name.replace('_', ' ')

                # Создаем изображение с динамической зависимостью от переменой speaking
                renpy.image(image_name, WhileSpeaking(short_name, change_name))

    addAllImage('m', 'mazelov')
    addAllImage('t', 'toxa')
    addAllImage('d', 'drake')
    addAllImage('s', 'stint')

    # Функция для проигрываения музыки без долгого вступления
    # если игрок пропускает переходы
    def playSkipMus(mus_name):
        mus_name = f'music/{mus_name}.mp3'
        if renpy.is_skipping(): 
            renpy.music.stop()
            renpy.music.play(mus_name, loop=True)

# Создание слоя для темного фильтра
init python:
    # Переопределение слоёв
    config.layers = ['master', 'transient', 'black_filter' ,'screens', 'overlay']
    # Добавление нового слоя для затемнения
    renpy.add_layer('black_filter', 'master')

# Создание нового голосового канала для звука "голоса" при печатанье текста
init:
    init python:
        renpy.music.register_channel('vox', 'music', loop=True)

# Определение трансформаций
init:
    transform step:
        xanchor 1.0 yanchor 1.0
        xpos 1.0 ypos 1.0
        linear 0.45 xpos 0.85 ypos 1.0 

    transform took_step:
        xanchor 1.0 yanchor 1.0
        xpos 0.85 ypos 1.0

    transform step_back_1:
        xanchor 1.0 yanchor 1.0
        linear 0.75 xpos 0.925 ypos 1.0 

    transform step_back_2:
        xanchor 1.0 yanchor 1.0
        linear 0.85 xpos 1.0 ypos 1.0 

    transform stumbled:
        xanchor 1.0 yanchor 1.0
        xpos 1.0 ypos 1.0
        linear 0.5 xpos 0.975
        linear 0.05 xpos 0.965
        linear 0.15 xpos 1.0

# Определение персонажей игры.
define m = Character('mazellovvv', color='#8d6555', image='mazelov', callback=Speaker('m', 'mazelov'))
define t = Character('t2x2', color='#6c5a82', image='toxa',callback=Speaker('t', 'toxa'))
define d = Character('drakeoffc', color='#cdc04f', image='drake', callback=Speaker('d', 'drake'))
define s = Character('stintik', color='#509a5d', image='stint',callback=Speaker('s', 'stint'))

# Определяем переход с долгой тряской
define vpunch3 = Move ((0, 10), (0, -10),.10, bounce=True, repeat=True, delay=.275*5)


# Игра начинается здесь:
label start:

    show text'''
    {color=#f60104}{size=96}Внимание!{/size}{/color}{p}{p}{color=#cfcfcf}В этой игре присутсвуют упоминания крови и неприятные темы. В связи с этим настоятельно не рекомендуем к прохождению данную визуальную новеллу: детям, беременным женщинам, людям с тонкой душевной организацией или с проблемами сердечно-сосудестой системы. Мы не несём цели кого-либо оскорбить и ни к чему не призываем, наш материал носит сугубо развлекательный характер.{p}{p}
    Приятного прохождения!{/color}
    '''
    pause

    # Отключаем скип пауз и переходов
    $ _dismiss_pause = False
    # # Устанавливаем скорость показа обычного текста, чтобы каждый раз не делать это в ручную
    # $ preferences.text_cps = text_speed

    jump act1
    return

# Акт 1
# Сцены с Мазеловым на улице, в подъезде и квартире Тохи
label act1:

    # Показываем на новом слое прозрачный темный цвет для затемнения всех спрайтов
    show black onlayer black_filter:
        alpha 0.4
    
    $ _skipping = False
    play music late loop fadein 2 fadeout 5
    scene bg street with Fade(2, 3, 2)
    $ _skipping = True
    $ playSkipMus('late')

    show mazelov normal at right

    narrator '''
        Илья быстрыми шагами шёл по пустой улице, потирая
        руки от холода. Серое небо нависало над городом, обещая скорый дождь.
    '''

    narrator '''
        Подойдя к старому подъезду, он остановился и посмотрел наверх, где за грязным окном на третьем этаже должен был находиться его друг Антон. {w=4.5} Но свет внутри квартиры не горел.
    '''

    m '{cps=[ts]}Странно, — пробормотал Илья, доставая из кармана телефон.{w} Сигнала не было.{/cps}'

    # Отключаем скип при всяком переходе
    $ _skipping = False
    play music home loop fadein 1 fadeout 10
    scene bg entrance with Fade(3, 5, 2)
    $ _skipping = True
    $ playSkipMus('home')

    show mazelov normal at right

    narrator '''
        Он толкнул скрипучую дверь подъезда и начал подниматься по тёмной лестнице. Каждый шаг отдавался эхом, которое будто сопровождало его шёпотом.
    '''

    narrator '''
        Поднявшись к нужной двери, он заметил, что та приоткрыта. Это уже не просто странно.
    '''

    m '{cps=[ts]}Антон? — позвал Илья, заглядывая внутрь. Ответа не последовало.{/cps}'
   
    scene bg kitchen with dissolve

    narrator '''
        Квартира встретила его гнетущей тишиной. Света действительно не было, и только тусклый дневной свет пробивался через занавешенные окна. В воздухе висел неприятный, затхлый запах, от которого Мазеллов поморщился.
    '''

    $ speaking = 'm'
    show mazelov looking at stumbled


    narrator '''
        Он сделал осторожный шаг вперёд и споткнулся о что—то мягкое. Опустив взгляд, он увидел разбросанные по полу вещи — старую одежду, разорванные газеты, пустые коробки.
    '''

    m @ asks '{cps=[ts]}Антон, ты дома? — громче спросил он, но снова — тишина.{/cps}'

    narrator '''
        Илья замер, прислушиваясь. Где—то в глубине квартиры послышался едва уловимый звук, напоминающий шорох. Это было похоже на то, как что—то или кто— то двигается по полу. Он напрягся, чувствуя, как по спине пробежал холодок.
    '''

    narrator 'Из темноты показалась фигура — это был Антон.{w=2.5}{nw}'

    $ speaking = 't'
    show toxa normal at left

    narrator '''
        Его лицо выглядело измождённым, рука была туго перевязана грязным бинтом, сквозь который местами проступали пятна засохшей крови. Одежда его была помята, а волосы растрёпаны.
    ''' 

    m '{cps=[ts]}Антон, что с тобой случилось? — воскликнул Илья, делая шаг навстречу.{/cps}' 

    $ speaking = 'm'
    show mazelov normal at step
    pause 1.0

    narrator '''
        Антон поднял взгляд, но не ответил сразу. Его губы дрожали, как будто он собирался что—то сказать, но слова застряли в горле. Вместо этого он тихо прохрипел:
    '''

    hide mazelov

    t '{cps=[ts/4]}Илья...{w=1} я рад что ты пришел...{/cps}'

    narrator 'Илья шагнул в коридор и почувствовал, как воздух стал гуще, насыщеннее.'

    narrator 'Пахло чем—то сладковатым, едва уловимым, но при этом настолько тяжёлым, что его желудок неприятно сжался.'

    narrator 'Он нахмурился, бросив взгляд на друга, но тот лишь
    молча указал на открытую дверь в глубине квартиры.'

    t asks '{cps=[ts/3]}В комнату. Там поговорим,{/cps}{cps=[ts/2]} — сухо сказал Антон.{/cps}'

    scene bg room with dissolve

    narrator '''
        Проходя внутрь, Илья старался не обращать внимания на неприятный запах, который будто обволакивал его.
    '''
    $ speaking = 'm'
    show mazelov looking:
        xanchor 1.0 yanchor 1.0
        xpos 1.1 ypos 1.0
        linear 2.75 xpos 1.0 ypos 1.0 
    pause 2.75

    narrator '''
        Он замер у порога, оглядывая беспорядок вокруг: на полу валялись какие-то бумаги, порванные книги и старые коробки. Ему на глаза попалась стопка листовок, часть из которых была разбросана по полу.
    '''
    narrator '''
        Он нагнулся, чтобы поднять одну из них. Листовка оказалась изрядно помятой, с текстом, который тут же привлёк его внимание. Строки были напечатаны криво, как будто на старом принтере, а шрифт казался странно неестественным.
    '''
    jump act2
    return

# Акт 2
# Сцена в кафе с Дрейком и Стинтом
label act2:
    
    $ _skipping = False
    play music bc loop fadein 2 fadeout 10
    scene cutscenes cafe with Fade(3, 7, 2)
    $ _skipping = True
    $ playSkipMus('bc')

    narrator '''
        В небольшой уютной кафешке у окна сидели двое друзей — Денис и Максим. За окном лениво шел дождь, оставляя тонкие дорожки на стекле, а внутри слышался тихий гул разговоров и звяканье чашек.
    '''

    narrator '''
        Денис, развалившись на мягком диване, скользил пальцем по экрану телефона, увлечённо листая ленту новостей. Максим напротив лениво потягивался, явно скучая.
    '''

    scene bg cafe with dissolve

    $ speaking = 's'
    show stint normal at left
    show drake normal at right

    s '{cps=[ts]}Ты хоть иногда сюда смотри, а? — сказал Максим, поднимая бровь.{/cps}'

    s '{cps=[ts]}Я же тут сижу, а не в твоём телефоне.{/cps}'

    d '{cps=[ts]}Подожди, тут реально что-то странное, — отмахнулся Дрейк, не отрывая глаз от экрана.{/cps}'

    d '{cps=[ts]}Его выражение лица стало серьёзнее. — Слушай... Ты слышал об этом вирусе?{/cps}'

    narrator 'Максим отложил чашку и нахмурился.'

    s focused '{cps=[ts]}Каком ещё вирусе? Что за бред?{/cps}'

    d looking '{cps=[ts]}Пишут, что у животных в разных частях города начали обнаруживать повреждения мозга. Они становятся агрессивными, бросаются на людей и...{w=4}{nw}{/cps}'

    d '{cps=[ts]}Денис замолчал, вчитавшись в текст на экране.{w=1.75} И едят всё подряд. Как будто голодные до безумия.{/cps}'

    s normal '{cps=[ts]}Да ладно! — фыркнул Максим, скрестив руки на груди.{/cps}'

    s '{cps=[ts]}Очередная байка для кликбейта.{/cps}'

    d '{cps=[ts]}Ага, а вот это тоже байка? — Денис повернул экран телефона, показывая жуткую фотографию.{/cps}'

    narrator '''
        На ней была запечатлена собака с диким взглядом,окровавленной мордой и вздыбленной шерстью. Она стояла в луже, а вокруг виднелись следы борьбы.
    '''

    $ speaking = 's'
    show stint focused at left

    narrator 'Максим нахмурился, на его лице появилась тень тревоги.'

    s smiling '{cps=[ts]}Не бойся, ты не заразишься. —пошутил Стинт стараясь разрядить атмосферу.{/cps}'

    d angry '{cps=[ts]}Это по-твоему смешно? Ты понимаешь, что это происходит здесь, в нашем городе. — сказал Денис, голосом, в котором смешались возбуждение и беспокойство.{/cps}'

    d rage '{cps=[ts]}Говорят, вирус распространяется быстро, и пока никто не знает, как с этим бороться......{w=2.5}Вирус достигает мозга и вызывает рост аномальных опухолей, состоящих из видоизменённых глиальных клеток.{/cps}'

    d '{cps=[ts]}Эти опухоли начинают давить на участки, отвечающие за контроль агрессии и чувство насыщения.{/cps}'

    d normal '{cps=[ts]}Пути заражения, контакт с заражённой кровью или слюной, укусы, прямое употребление заражённой пищи. — бормотал себе под нос Денис, продолжая читать статью.{/cps}'

    s normal '{cps=[ts]}Ну и дела...{w=1.5} еще и Братишкин пропал, какая-то невезучая неделя выдалась{/cps}'

    narrator '''
        Макс задумчиво откинулся на спинку стула, окинув взглядом посетителей кафе. За окном дождь становился всё сильнее, как будто город готовился к чему-то недоброму.
    '''

    jump act3
    return

# Сцена Мазеловым и Тохой в квартире 
# Акт 3
label act3:

    $ _skipping = False
    play music hunger loop fadein 2 fadeout 10
    scene cutscenes mazelov_leaflet with Fade(3, 7, 2)
    $ _skipping = True
    $ playSkipMus('hunger')

    narrator '''
    Илья стоял посреди комнаты, держа в руках одну из
    листовок. Его взгляд был прикован к изображению человека, знакомого до боли. Это был их общий знакомый - Вова.
    '''

    scene cutscenes leaflet with dissolve

    narrator '''
    Текст на листовке гласил: {i}"Пропал без вести. Последний раз его видели около двух недель назад. Просим всех, кто располагает информацией, связаться с нами.{i}"
    '''

    narrator '''
    Илья почувствовал, как холод прокатился по его спине. Он повернулся к Антону, который всё ещё стоял у стены
    '''

    scene bg room with dissolve

    show mazelov nerd at right

    m '{cps=[ts]}Это что? — голос Ильи дрогнул.{/cps}' 

    $ speaking = 't'
    show toxa looking at left
    
    narrator 'Антон молчал, глядя куда-то мимо Мазеллова. Его лицо было пустым, как маска.'

    m '{cps=[ts]}Ты знаешь, где он? — Илья сжал листовку, делая шаг вперёд.{/cps}'

    $ speaking = 'm'
    show mazelov normal at step
    pause 1.0

    t says '{cps=[ts/3]}Я{w=0.5}.{w=0.5}.{w=0.5}.{/cps}{cps=[ts]} — Антон наконец заговорил, его голос был хриплым, будто выжатым.{/cps}'

    t '{cps=[ts/3]}Я не хотел, чтобы это случилось.{/cps}'

    show mazelov normal at took_step

    m asks '{cps=[ts]}Что случилось? Антон, ты меня пугаешь.{/cps}'

    narrator 'Илья подошёл ближе, но Антон резко вскинул руку, словно пытаясь его остановить.'

    t scared '{cps=[ts*2]}Не подходи! — выкрикнул он, а потом зажмурился, будто от боли.{/cps}'

    play sound kogti volume 0.5

    narrator '''
    Тишину разорвал звук скрипа — что-то тяжёлое двигалось по полу в соседней комнате. Илья замер, чувствуя, как кровь стынет в жилах.
    '''

    m scared '{cps=[ts]}Это что ещё такое? — выдавил он, оглядываясь.{/cps}'

    play sound ryichanie_sobaki loop volume 0.4

    narrator '''
        Из глубины квартиры донеслось низкое рычание, похожее на утробный стон. Оно становилось всё громче, сопровождаясь тяжёлыми шагами. Илья машинально сделал шаг назад.
    '''
    $ speaking = 'm'
    show mazelov terrified at step_back_1
    show mazelov terrified with vpunch3
    pause 1

    m '{cps=[ts]}Антон... — начал он, но его друг поднял на него глаза. Взгляд Антона был полон отчаяния и страха.{/cps}'

    $ speaking = 'm'
    show mazelov terrified at step_back_2
    pause 1

    narrator '''
        Илья сделал шаг назад, почувствовав, как что-то холодное и липкое касается его ноги. Он опустил взгляд и увидел кровавые пятна на полу, ведущие в сторону соседней комнаты. Теперь он знал, откуда исходил этот сладковатый запах.
    '''

    m '{cps=[ts/4]}Вова...{w=0.5}{/cps}{cps=[ts/2]} —ком в горле и поступавшая тошнота не дали ему договорить.{/cps}'

    $ _skipping = False
    stop sound fadeout 10
    stop music fadeout 10
    scene black with Fade(3, 5, 2) 
    $ _skipping = True
    $ if renpy.is_skipping(): renpy.music.stop(); renpy.sound.stop()


    show text '{sc}— Прости, Илья, — хрипло произнёс Антон, с трудом дыша. — ..Лаки хочет кушать.{w=30}{sc}' onlayer black_filter

    pause 10

    return