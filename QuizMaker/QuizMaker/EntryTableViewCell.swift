//
//  EntryTableViewCell.swift
//  QuizMaker
//
//  Created by Nene Yamasaki on 19/01/2019.
//  Copyright © 2019 Nene Yamasaki. All rights reserved.
//

import UIKit

class EntryTableViewCell: UITableViewCell {

    @IBOutlet weak var answerField: UITextField!
    @IBOutlet weak var questionField: UITextField!
    
    var delegate:EntryTableViewCellDelegate?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    func configure(for entry: QuizEntry){
        self.questionField.text = entry.question
        self.answerField.text = entry.answer
        answerField.delegate = self
        questionField.delegate = self
    }

}

extension EntryTableViewCell : UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool{
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        self.delegate!.didEndEditing(cell: self)
        self.delegate!.updateQuestion(for: self)
    }
}

protocol EntryTableViewCellDelegate {
    func updateQuestion(for cell: EntryTableViewCell)
    func didEndEditing(cell: EntryTableViewCell)
}
