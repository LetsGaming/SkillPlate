-- CREATE IF NOT EXISTS PROCEDURE (name VARCHAR,
--   instructions VARCHAR) 
--   BEGIN
--     INSERT INTO recipe (recipe_name,
--       recipe_instructions) VALUES 
--       (name, 
--         instructions);
--   END;
--
-- CREATE IF NOT EXISTS PROCEDURE AddCourse (course_in IN CLOB)
--   IS
--     course JSON_OBJECT_T := JSON_OBJECT_T(course_in);
--     recipe JSON_ARRAY_T := course.get_Array('recipes');
--     ingredients JSON_ARRAY_T := recipe.get_Array('ingredients');
CREATE OR REPLACE PROCEDURE insert_course_json (
    p_json_str IN CLOB
) AS
BEGIN
    --------------------------------------------------------
    -- 1. Insert/Merge into COURSE Table
    --------------------------------------------------------
    MERGE INTO course t
    USING (
        SELECT *
        FROM JSON_TABLE(p_json_str, '$'
            COLUMNS (
                course_id         INT          PATH '$.course_id',
                course_name       VARCHAR2(400) PATH '$.course_name',
                course_theme      VARCHAR2(100) PATH '$.course_theme',
                course_online     BOOLEAN      PATH '$.course_online',
                course_difficulty VARCHAR2(100) PATH '$.course_difficulty'
            )
        )
    ) s
    ON (t.course_id = s.course_id)
    WHEN NOT MATCHED THEN
        INSERT (course_id, course_name, course_theme, course_online, course_difficulty)
        VALUES (s.course_id, s.course_name, s.course_theme, s.course_online, s.course_difficulty);

    --------------------------------------------------------
    -- 2. Insert/Merge into RECIPE Table
    --------------------------------------------------------
    MERGE INTO recipe t
    USING (
        SELECT DISTINCT recipe_id, recipe_name, recipe_instructions
        FROM JSON_TABLE(p_json_str, '$.recipes[*]'
            COLUMNS (
                recipe_id           INT            PATH '$.recipe_id',
                recipe_name         VARCHAR2(600)  PATH '$.recipe_name',
                recipe_instructions VARCHAR2(32000) PATH '$.recipe_instructions'
            )
        )
    ) s
    ON (t.recipe_id = s.recipe_id)
    WHEN NOT MATCHED THEN
        INSERT (recipe_id, recipe_name, recipe_instructions)
        VALUES (s.recipe_id, s.recipe_name, s.recipe_instructions);

    --------------------------------------------------------
    -- 3. Insert/Merge into INGREDIENT Table
    --------------------------------------------------------
    MERGE INTO ingredient t
    USING (
        SELECT DISTINCT ingredient_id, ingredient_name, ingredient_type
        FROM JSON_TABLE(p_json_str, '$.recipes[*].ingredients[*]'
            COLUMNS (
                ingredient_id   INT           PATH '$.ingredient_id',
                ingredient_name VARCHAR2(200) PATH '$.ingredient_name',
                ingredient_type VARCHAR2(1000) PATH '$.ingredient_type'
            )
        )
    ) s
    ON (t.ingredient_id = s.ingredient_id)
    WHEN NOT MATCHED THEN
        INSERT (ingredient_id, ingredient_name, ingredient_type)
        VALUES (s.ingredient_id, s.ingredient_name, s.ingredient_type);

    --------------------------------------------------------
    -- 4. Insert/Merge into COURSE_RECIPES (Mapping Table)
    --    Uses NESTED PATH to bind the top level course to recipes
    --------------------------------------------------------
    MERGE INTO course_recipes t
    USING (
        SELECT course_id, recipe_id
        FROM JSON_TABLE(p_json_str, '$'
            COLUMNS (
                course_id INT PATH '$.course_id',
                NESTED PATH '$.recipes[*]' COLUMNS (
                    recipe_id INT PATH '$.recipe_id'
                )
            )
        )
    ) s
    ON (t.course_id = s.course_id AND t.recipe_id = s.recipe_id)
    WHEN NOT MATCHED THEN
        INSERT (course_id, recipe_id)
        VALUES (s.course_id, s.recipe_id);

    --------------------------------------------------------
    -- 5. Insert/Merge into RECIPE_INGREDIENTS (Mapping Table)
    --    Uses double NESTED PATHs to tie recipe pieces to ingredients
    --------------------------------------------------------
    MERGE INTO recipe_ingredients t
    USING (
        SELECT recipe_id, ingredient_id, amount, unit
        FROM JSON_TABLE(p_json_str, '$'
            COLUMNS (
                NESTED PATH '$.recipes[*]' COLUMNS (
                    recipe_id INT PATH '$.recipe_id',
                    NESTED PATH '$.ingredients[*]' COLUMNS (
                        ingredient_id INT           PATH '$.ingredient_id',
                        amount        DECIMAL(10,2) PATH '$.amount',
                        unit          VARCHAR2(50)  PATH '$.unit'
                    )
                )
            )
        )
    ) s
    ON (t.recipe_id = s.recipe_id AND t.ingredient_id = s.ingredient_id)
    WHEN NOT MATCHED THEN
        INSERT (recipe_id, ingredient_id, amount, unit)
        VALUES (s.recipe_id, s.ingredient_id, s.amount, s.unit);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END insert_course_json;
/

CREATE OR REPLACE FUNCTION get_course_json (
    p_course_id IN INT
) RETURN CLOB IS
    v_json_result CLOB;
BEGIN
    SELECT JSON_OBJECT(
        'course_id'         VALUE c.course_id,
        'course_name'       VALUE c.course_name,
        'course_theme'      VALUE c.course_theme,
        'course_online'     VALUE CASE WHEN c.course_online = 1 THEN TRUE ELSE FALSE END,
        'course_difficulty' VALUE c.course_difficulty,
        'recipes'           VALUE (
            -- Subquery to aggregate recipes into a JSON Array
            SELECT JSON_ARRAYAGG(
                JSON_OBJECT(
                    'recipe_id'           VALUE r.recipe_id,
                    'recipe_name'         VALUE r.recipe_name,
                    'recipe_instructions' VALUE r.recipe_instructions,
                    'ingredients'         VALUE (
                        -- Nested Subquery to aggregate ingredients for this specific recipe
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'ingredient_id'   VALUE i.ingredient_id,
                                'ingredient_name' VALUE i.ingredient_name,
                                'ingredient_type' VALUE i.ingredient_type,
                                'amount'          VALUE ri.amount,
                                'unit'            VALUE ri.unit
                            ) RETURNING CLOB
                        )
                        FROM recipe_ingredients ri
                        JOIN ingredient i ON ri.ingredient_id = i.ingredient_id
                        WHERE ri.recipe_id = r.recipe_id
                    )
                ) RETURNING CLOB
            )
            FROM course_recipes cr
            JOIN recipe r ON cr.recipe_id = r.recipe_id
            WHERE cr.course_id = c.course_id
        )
    )
    INTO v_json_result
    FROM course c
    WHERE c.course_id = p_course_id;

    RETURN v_json_result;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN '{}'; -- Return empty JSON object if course doesn't exist
    WHEN OTHERS THEN
        RAISE;
END get_course_json;
/
