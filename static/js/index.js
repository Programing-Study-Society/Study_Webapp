(async () =>{
    // データの取得
    const res = await fetch('/api/todos');
    if (!res.ok) {
        alert("データが取得できませんでした");
    }
    // データをJSON形式に変形
    const data = await res.json();
    console.log(data);
    //データを一つずつ表示
	data.forEach((element) => {
		const $todoTemplate = document.getElementById('todo-template').content.cloneNode(true);
		$todoTemplate.querySelector('.todo-title').innerText = element['title'];
        $todoTemplate.querySelector('.todo-description').innerText = element['description'];
        $todoTemplate.querySelector('.update-todo-button').setAttribute('href', '../html/update.html?id=' + element['id'])
        $todoTemplate.querySelector('.delete-todo-button').setAttribute('href', '../html/delete.html?id=' + element['id'])
		document.getElementById('todo-list').appendChild($todoTemplate);
	});
    
})();
