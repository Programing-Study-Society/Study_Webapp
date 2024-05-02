(async () => {
    // タイトルと詳細を入力フォームから取得
    const $title = document.getElementById('input-title');
    const $description = document.getElementById('input-description');
    
    // TODOのIDを取得
    const id = getId(window.location.href)
    // 現在のTodoを取得
    const originalRes = await fetch("http://localhost:8000/api/todo/" + id);
    // エラーの時に警告文を表示
    if (!originalRes.ok) {
        alert("データが取得できませんでした");
    }
    // データの形式をjsonに変換
    const originalData = await originalRes.json();
    // 現在のTodoをフォームに入れておく
    $title.value = originalData["todo"]["title"];
    $description.value = originalData["todo"]["description"];
    
    const updateTodo = async (e) =>{
    
        // 元々の動作を解除
        e.preventDefault();
        
        // サーバーに送信
        const res = await postData(
            "/api/update", 
            {
                "id": id,
                "title": $title.value,
                "description": $description.value
            }
        );
        // エラーの時に警告文を表示
        if (!res.ok) {
            alert("Todoの更新に失敗しました");
        }
        // 一覧の画面に戻る
        window.location.href = "/"
    }
    
    // 送信ボタンを押したときにupdateTodo関数の挙動をさせる
    document.querySelector("form.update-todo-form").addEventListener('submit', updateTodo);
})();
