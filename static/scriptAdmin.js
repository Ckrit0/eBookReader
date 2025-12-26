/**
 * 클릭 애니메이션 추가 및 이중클릭 방지
 * @param {HTML Button Tag} target 
 */
function imWorking(target){
    target.onclick = null
    target.innerText = '🌀'
    target.classList.add('working')
}

/**
 * 이전 페이지로 이동
 */
function prevPage(){
    if(confirm("이전 페이지로 이동하시겠습니까?")){
        history.go(-1)
    }
}

/**
 * 수정 취소시 새로고침
 * @returns 
 */
function cancelChange(){
    if(!confirm("수정을 취소하시겠습니까?")){
        return
    }
    window.location.href = window.location.href
}

/**
 * url로 post 요청하기
 * @param {String} url
 * @param {JSON} data 
 */
function postAPI(url, data){
    let form = document.createElement('form')
    form.method = 'post'
    form.action = url
    document.body.appendChild(form)
    for(let key in data){
        let dataInput = document.createElement('input')
        dataInput.name = key
        dataInput.value = data[key]
        form.appendChild(dataInput)
    }
    form.submit()
}

// 도서 추가 관련
function insertBook(){
    let bookName = prompt("도서명을 입력하세요")
    let targetURL = "/insert/" + bookName
    postAPI(targetURL,{})
}

/**
 * 글 쓰기 페이지 이동
 */
function insertVolume(){
    location.href = '/insert/' + bookInfo['name']
}

/**
 * 글 수정하기 페이지 이동
 */
function modifyVolume(){
    location.href = '/insert/' + bookInfo['name'] + '/' + bookInfo['volume']
}

/**
 * 글 작성 DB 적용
 */
async function insertContents(){
    let targetVolume = ''
    let targetTag = document.getElementById("insVolume")
    if(targetTag.tagName == 'INPUT'){
        targetVolume = document.getElementById("insVolume").value
    }else{
        targetVolume = document.getElementById("insVolume").innerText
    }
    if(bookInfo['lastVolume'] <= targetVolume && !confirm(targetVolume + "권(화)의 내용을 수정 하시겠습니까?")){
        return
    }
    let contents = document.getElementById("contentsArea").value
    // 엔터가 두번 이상이면 한번만 남김
    while(contents.indexOf('\n\n') >= 0){
        contents = contents.replaceAll('\n\n','\n')
    }
    // 공백이 두번 이상이면 한번만 남김
    while(contents.indexOf('  ') >= 0){
        contents = contents.replaceAll('  ',' ')
    }
    let contentList = []
    let tempContentList = contents.split('\n')
    for(var i in tempContentList){
        // 한 줄의 길이가 1000글자(DB에 셋팅된 용량)를 넘기면 다음줄로 넘김
        if(tempContentList[i].length <= 1000){
            contentList.push(tempContentList[i])
        }else{
            for(var len=0;len<tempContentList[i].length;len=+1000){
                contentList.push(tempContentList[i].slice(len,len+1000))
            }
        }
    }
    // 내용이 너무 길지 않도록 나눠서 업로드
    let targetURL = '/insert/' + bookInfo['name'] + '/' + targetVolume
    let bookId = bookInfo['name'] + '-' + targetVolume
    let chunkSize = 500
    let totalChunk = Math.ceil(contentList.length/chunkSize)
    for(let chunkIndex=0;chunkIndex<totalChunk;chunkIndex++){
        let data = new FormData()
        for(var i=chunkIndex*chunkSize;i<(chunkIndex*chunkSize+chunkSize);i++){
            if(i < contentList.length){
                data.append(i,contentList[i])
            }
        }
        data.append('bookId', bookId)
        data.append('totalChunk', totalChunk)
        data.append('chunkIndex', chunkIndex)
        await fetch(targetURL,{
            method : 'POST',
            body : data
        }).then((res)=>{
            res.json()
        }).then((result)=>{
            console.log(result)
            if(result == 100){
                window.location.href = '/admin/' + bookInfo['name']
            }
        })
    }
}



/**
 * 대상 수정을 위해 TAG 및 기능 변경
 * @param {"book" or "vol" or "line"} type 
 * @param {String} lineId 
 */
function changeInput(type, lineId){
    // 수정할 태그를 Input으로 변경
    let target = document.getElementById('box' + type + lineId)
    let text = target.innerText
    if(type == "vol"){ // A Tag 무력화
        target = target.parentElement
    }else if(type == "book"){
        target = target.parentElement
    }
    target.outerHTML = "<input id='box" + type + lineId + "' value='" + text + "'/>"
    
    // 수정버튼의 기능 변경
    let targetBtn = document.getElementById('mod' + type + lineId)
    targetBtn.onclick = ()=>{updateTarget(type, lineId)}
    targetBtn.innerText = '✅'

    // X 버튼의 기능 변경 (삭제에서 수정 취소로..)
    let targetDelBtn = document.getElementById('del' + type + lineId)
    targetDelBtn.onclick = ()=>{cancelChange()}

    // Input에 focus 및 keydown EventListener 설정
    let targetInput = document.getElementById('box' + type + lineId)
    targetInput.focus()
    var tempValue = '' // 커서를 맨 뒤로 보내기 위한 과정
    tempValue = targetInput.value
    targetInput.value = ''
    targetInput.value = tempValue
    targetInput.addEventListener('keydown',(e)=>{
        if(e.key == 'Enter'){
            updateTarget(type, lineId)
        }else if(e.key == 'Escape'){
            cancelChange()
        }
    })
}

/**
 * 대상 수정을 위해 DATA를 수집 및 POST API 요청
 * @param {"book" or "vol" or "line"} type 
 * @param {String} lineId 
 */
function updateTarget(type, lineId){
    let targetBtn = document.getElementById('mod' + type + lineId)
    imWorking(targetBtn)
    let data = {
        'data' : document.getElementById('box' + type + lineId).value
    }
    let targetURL = ""
    if(type == "book"){
        targetURL = "/update/" + lineId
    }else if(type == "vol"){
        targetURL = "/update/" + bookInfo['name'] + "/" + lineId
    }else if(type == "line"){
        let redirectionLine = document.getElementById('headLine').value
        targetURL = "/update/" + bookInfo['name'] + "/" + bookInfo['volume'] + "/" + lineId + "/" + redirectionLine
    }
    postAPI(targetURL, data)
}

/**
 * 대상 삭제를 위해 POST API 요청
 * @param {"book" or "vol" or "line"} type 
 * @param {String} lineId 
 * @returns 
 */
function deleteTarget(type, lineId){
    let typeName = ""
    let targetURL = ""
    if(type == "book"){
        typeName = "도서를"
        targetURL = "/delete/" + lineId
    }else if(type == "vol"){
        typeName = "권(화)을"
        targetURL = "/delete/" + bookInfo['name'] + "/" + lineId
    }else if(type == "line"){
        typeName = "줄을"
        targetURL = "/delete/" + bookInfo['name'] + "/" + bookInfo['volume'] + "/" + lineId
    }
    if(!confirm('선택한 ' + typeName + ' 삭제하시겠습니까?')){
        return
    }
    let targetBtn = document.getElementById('del' + type + lineId)
    imWorking(targetBtn)
    postAPI(targetURL, {})
}

/**
 * 컨텐츠 에어리어에 focus주고 ctrl+s 키 저장기능 설정
 */
function contentsAreaSetting(){
    let c_area = document.getElementById('contentsArea')
    c_area.focus()
    c_area.addEventListener('keydown',(e)=>{
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            insertContents()
        }
    })
}
