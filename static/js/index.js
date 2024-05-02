(async () =>{
    // データの取得
    const res = await fetch('/api/todos');
    // エラーの時に警告文を表示
    if (!res.ok) {
        alert("データが取得できませんでした");
    }
    // データをJSON形式に変形
    const data = await res.json();
    // データを一つずつ表示
	data["todos"].forEach((element) => {
        // todoを表示するためのテンプレートを取得してクローンを作成
		const $todoTemplate = document.getElementById('todo-template').content.cloneNode(true);
        // タイトルと説明をクローンに入力
		$todoTemplate.querySelector('.todo-title').innerText = element['title'];
        $todoTemplate.querySelector('.todo-description').innerText = element['description'];
        // 編集と削除のボタンにリンクを設定
        $todoTemplate.querySelector('.update-todo-button').setAttribute('href', '../html/update.html?id=' + element['id'])
        $todoTemplate.querySelector('.delete-todo-button').setAttribute('href', '../html/delete.html?id=' + element['id'])
        // 設定が完了したクローンを下に追加
		document.getElementById('todo-list').appendChild($todoTemplate);
	});
    
})();
