one_word_replacments = ["врач", "медицинская сестра",
                        "бухгалтер", "программист",
                        "экономист", "водитель",
                        "вахтер", "агроном", "уборщик", "библиотекарь", "слесарь", "техник",
                        "заведующий лабораторией",
                        "ведущий научный сотрудник",
                        "главный научный сотрудник",
                        "заместитель директора", "лаборант", "монтер",
                        "инженер"]
one_word_replacments = dict([(i, i) for i in one_word_replacments])
one_word_replacments["медицинский брат"] = "мед. брат/сестра"
one_word_replacments["медицинская сестра"] = "мед. брат/сестра"
one_word_replacments["фельдшер"] = "мед. брат/сестра"
one_word_replacments["сторож"] = "вахтер"
one_word_replacments["дворник"] = "уборщик"
one_word_replacments["диспетчер"] = "вахтер"
one_word_replacments["комендант"] = "вахтер"
one_word_replacments["озеленитель"] = "уборщик"
one_word_replacments["ответственный дежурный"] = "вахтер"
one_word_replacments["столяр"] = "подсобный рабочий"
one_word_replacments["токарь"] = "подсобный рабочий"
one_word_replacments["слесарь"] = "подсобный рабочий"
one_word_replacments["подсобный рабочий"] = "подсобный рабочий"
one_word_replacments["гардеробщик"] = "вахтер"
one_word_replacments["гардеробщица"] = "вахтер"
one_word_replacments["контролер кпп"] = "вахтер"
one_word_replacments["тракторист"] = "водитель"
one_word_replacments["санитар"] = "санитарка"
one_word_replacments["облицовщик-плиточник"] = "подсобный рабочий"
one_word_replacments["кладовщик"] = "вахтер"

