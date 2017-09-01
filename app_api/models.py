import tensorflow as tf
import numpy as np
tf.logging.set_verbosity(tf.logging.INFO)

def ANN_train(training_input, training_target,epochs=1,validation_size=6):

    test_input = training_input[:validation_size,:]
    test_target = training_target[:validation_size]
    train_input = training_input[validation_size+1:,:]
    train_target = training_target[validation_size+1:]

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(test_input)},
                                                        num_epochs=1,
                                                        shuffle=False)

    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[67])]


    # Build a DNN
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[300],
                                            n_classes=5,
                                            model_dir="./tmp/course_difficulty_model",
                                            activation_fn=tf.nn.relu)

    # Define the training inputs
    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(train_input)},
                                                        y=np.array(train_target),
                                                        num_epochs=epochs,
                                                        shuffle=True)

    # Train model.
    classifier.train(input_fn=train_input_fn)

    predictions = list(classifier.predict(input_fn=predict_input_fn))
    predicted_classes = [int(p["classes"][0]) for p in predictions]

    correct_prediction = np.equal(predicted_classes,test_target)
    accuracy = float(sum(correct_prediction))/len(test_target)
    print (predicted_classes)
    print (accuracy)

def ANN_predict(new_samples):
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[67])]

    # Build a DNN
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[300],
                                            n_classes=5,
                                            model_dir="./tmp/course_difficulty_model",
                                            activation_fn=tf.nn.relu)


    predict_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(new_samples)},
                                                        num_epochs=1,
                                                        shuffle=False)


    predictions = list(classifier.predict(input_fn=predict_input_fn))
    predicted_classes = [int(p["classes"][0]) for p in predictions]

    return predicted_classes
