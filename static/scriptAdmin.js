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
    
}

// 볼륨 추가 관련
function insertVolume(){
    
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
        targetURL = "/update/" + bookInfo['name'] + "/" + bookInfo['volume']
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
        targetURL = "/delete/" + bookInfo['name'] + "/" + bookInfo['volume']
    }else if(type == "line"){
        typeName = "줄을"
        targetURL = "/delete/" + bookInfo['name'] + "/" + bookInfo['volume'] + "/" + lineId
    }
    if(!confirm('"선택한 ' + typeName + '" 삭제하시겠습니까?')){
        return
    }
    let targetBtn = document.getElementById('del' + type + lineId)
    imWorking(targetBtn)
    postAPI(targetURL, {})
}
