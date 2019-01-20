//
//  EntryTableViewController.swift
//  QuizMaker
//
//  Created by Nene Yamasaki on 19/01/2019.
//  Copyright © 2019 Nene Yamasaki. All rights reserved.
//

import UIKit

extension URLSession {
    func synchronouslyExecute(_ request:URLRequest) -> (Data?, URLResponse?, NSError?) {
        var data: Data?, response: URLResponse?, error: NSError?
        
        let semaphore = DispatchSemaphore(value: 0)
        
        dataTask(with: request, completionHandler: {
            data = $0; response = $1; error = $2 as NSError?
            semaphore.signal()
        }) .resume()
        let timeout = DispatchTime.now() + Double(10000000000) / Double(NSEC_PER_SEC)
        
        semaphore.wait(timeout: timeout)
        
        return (data, response, error)
    }
}

extension String {
    
    func fromBase64() -> String? {
        guard let data = Data(base64Encoded: self, options: Data.Base64DecodingOptions(rawValue: 0)) else {
            return nil
        }
        
        return String(data: data as Data, encoding: String.Encoding.utf8)
    }
    
    func toBase64() -> String? {
        guard let data = self.data(using: String.Encoding.utf8) else {
            return nil
        }
        
        return data.base64EncodedString(options: Data.Base64EncodingOptions(rawValue: 0))
    }
}

struct EntryConstants{
    static let entryCellReuseIdentifier = "entryCell"
    static let uploadCellReuseIdentifier = "uploadCell"
}

class EntryTableViewController: UITableViewController {
    var questions:[QuizEntry] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 2
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if section == 0{
            return questions.count + 1
        }
        else{
            return 1
        }
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if indexPath.section == 0{
            let cell = tableView.dequeueReusableCell(withIdentifier: EntryConstants.entryCellReuseIdentifier, for: indexPath) as! EntryTableViewCell
            if indexPath.row >= self.questions.count - 1{
                self.questions.append(QuizEntry(question:"", answer:""))
            }
            cell.configure(for: self.questions[indexPath.row])
            cell.delegate = self

            // Configure the cell...

            return cell
        }
        else{
            let cell = tableView.dequeueReusableCell(withIdentifier: EntryConstants.uploadCellReuseIdentifier, for: indexPath) as! UploadTableViewCell
            cell.delegate = self
            return cell
        }
    }
 

    /*
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}

extension EntryTableViewController: EntryTableViewCellDelegate{
    func updateQuestion(for cell: EntryTableViewCell) {
        let indexPath = self.tableView.indexPath(for: cell)
        self.questions[indexPath!.row] = QuizEntry(question:cell.questionField.text!, answer:cell.answerField.text!)
        print(self.questions)
    }
    
    func didEndEditing(cell: EntryTableViewCell) {
        let indexPath = self.tableView.indexPath(for: cell)
        if indexPath!.row == questions.count - 1 && cell.questionField.text! != "" && cell.answerField.text! != ""{
            self.tableView.insertRows(at:[IndexPath(row: self.questions.count, section: 0)], with: .bottom)
//            self.questions.append(QuizEntry(question:"", answer:""))
        }
    }
}

struct RequestData: Codable{
    var quiz_data:[QuizEntry]
    var set_id: String
}

extension EntryTableViewController: UploadCellDelegate{
    func uploadData(){
        let url = URL(string: "https://quiet-temple-14701.herokuapp.com/chatbot/quiz")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        try! request.httpBody = JSONEncoder().encode(RequestData(quiz_data: self.questions, set_id: "random"))
        let (data, response, error) = URLSession.shared.synchronouslyExecute(request)
        print(response)
    }
}
